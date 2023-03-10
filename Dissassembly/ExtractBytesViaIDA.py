# *******************************************************************************
#  * Copyright 2017 McGill University All rights reserved.
#  *
#  * Licensed under the Apache License, Version 2.0 (the "License");
#  * you may not use this file except in compliance with the License.
#  * You may obtain a copy of the License at
#  *
#  *     http://www.apache.org/licenses/LICENSE-2.0
#  *
#  * Unless required by applicable law or agreed to in writing, software
#  * distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.
#  *******************************************************************************/

import json
import idaapi
import idautils
import idc
import os
import binascii

print('Kam1n0 script for idapro is now running...')
print('Waiting for idapro...')

idc.auto_wait()
idaapi.auto_wait()#idaapi.autoWait()
print('start persisting...')


def _iter_extra_comments(ea, start):
    end = idaapi.get_first_free_extra_cmtidx(ea, start)
    lines = [idaapi.get_extra_cmt(ea, idx) for idx in
             range(start, end)]
    lines = [line if line else '' for line in lines]
    return "\n".join(lines)


def get_comments(ea):
    comments = []
    text = idc.get_cmt(ea,1) #RptCmt(ea)
    if text and len(text) > 0:
        comments.append({'type':'repeatable', 'comment': text, 'offset' : str(hex(ea)).rstrip("L").upper().replace("0X", "0x")})
    text = idc.get_cmt(ea,0)#Comment(ea)
    if text and len(text) > 0:
        comments.append({'type':'regular', 'comment': text, 'offset' : str(hex(ea)).rstrip("L").upper().replace("0X", "0x")})
    text = _iter_extra_comments(ea, idaapi.E_PREV)
    if text and len(text) > 0:
        comments.append({'type':'anterior', 'comment': text, 'offset' : str(hex(ea)).rstrip("L").upper().replace("0X", "0x")})
    text = _iter_extra_comments(ea, idaapi.E_NEXT)
    if text and len(text) > 0:
        comments.append({'type':'posterior', 'comment': text, 'offset' : str(hex(ea)).rstrip("L").upper().replace("0X", "0x")})
    return comments


def get_apis(func_addr):
    calls = 0
    apis = []
    flags = get_func_attr(func_addr, FUNCATTR_FLAGS)#GetFunctionFlags(func_addr)
    # ignore library functions
    if flags & FUNC_LIB or flags & FUNC_THUNK:
        return calls, apis
    # list of addresses
    dism_addr = list(FuncItems(func_addr))
    for instr in dism_addr:
        tmp_api_address = ""
        if idaapi.is_call_insn(instr):
            # In theory an API address should only have one xrefs
            # The xrefs approach was used because I could not find how to
            # get the API name by address.
            for xref in XrefsFrom(instr, idaapi.XREF_FAR):
                if xref.to is None:
                    calls += 1
                    continue
                tmp_api_address = xref.to
                break
            # get next instr since api address could not be found
            if tmp_api_address == "":
                calls += 1
                continue
            api_flags = get_func_attr(tmp_api_address, FUNCATTR_FLAGS)#GetFunctionFlags(tmp_api_address)
            # check for lib code (api)
            if api_flags & idaapi.FUNC_LIB == True or api_flags & idaapi.FUNC_THUNK:
                tmp_api_name = get_name(tmp_api_address, ida_name.GN_VISIBLE | calc_gtn_flags(0, tmp_api_address)) #NameEx(0, tmp_api_address)
                if tmp_api_name:
                    apis.append(tmp_api_name)
            else:
                calls += 1
    return calls, apis


rebase = int(os.getenv('K_REBASE', 0))
cleanStack = int(os.getenv('K_CLEANSTACK', 0))
if rebase == 1:
    idaapi.rebase_program(-1 * idaapi.get_imagebase(), 0)

file_name = os.path.splitext(idc.get_idb_path())[0] #os.path.splitext(idc.GetIdbPath())[0]
binary_name = idaapi.get_input_file_path()
print(binary_name)
callees = dict()
funcmap = dict()
data = dict()
data['name'] = binary_name
data['md5'] = idautils.GetInputFileMD5().hex().upper()


for seg_ea in Segments():
    for function_ea in Functions(get_segm_start(seg_ea), get_segm_end(seg_ea)):#Functions(SegStart(seg_ea), SegEnd(seg_ea)):
        # fill call graph
        # For each of the incoming references
        for ref_ea in CodeRefsTo(function_ea, 0):
            # Get the name of the referring function
            caller_name = get_func_name(ref_ea)#GetFunctionName(ref_ea)
            # Add the current function to the list of functions
            # called by the referring function
            callees[caller_name] = callees.get(caller_name, set())
            callees[caller_name].add(function_ea)

data['architecture'] = {}
info = idaapi.get_inf_structure()
data['architecture']['type'] = info.procName.lower();
data['architecture']['size'] = "b32"
if info.is_32bit():
    data['architecture']['size'] = "b32"
if info.is_64bit():
    data['architecture']['size'] = "b64";
if idaapi.cvar.inf.version >= 700:
    data['architecture']['endian'] = "be" if idaapi.cvar.inf.is_be() else "le";
else:
    data['architecture']['endian'] = "be" if idaapi.cvar.inf.mf else "le";
if info.procName.lower().startswith('mips'):
    data['architecture']['type'] = 'mips'
if info.procName.lower().startswith('68330'):
    data['architecture']['type'] = 'mc68'

data['ida_compiler'] = idaapi.get_compiler_name(info.cc.id)

data['bytes'] = list()

for seg_ea in Segments():
    for function_ea in Functions(get_segm_start(seg_ea), get_segm_end(seg_ea)):#Functions(SegStart(seg_ea), SegEnd(seg_ea)):
        f_name = get_func_name(function_ea) #GetFunctionName(function_ea)

        # optional
        funcfc = idaapi.FlowChart(idaapi.get_func(function_ea))
        # basic bloc content
        for bblock in funcfc:
            for head in Heads(bblock.start_ea, bblock.end_ea):                
                bytesAddr = idc.get_bytes(head, idc.get_item_size(head))
                bytesD = "".join([ ("%0.2x" % bytesAddr[i]) for i in range(len(bytesAddr))])
                #bytesD = "".join(["{:02x}".format(c) for c in bytesAddr])                
                data['bytes'].append( bytesD )
                
with open('%s_bytes.json' % (file_name), 'w') as outfile:
    json.dump(data, outfile, ensure_ascii=False)

#idc.Exit()
idc.qexit(0)
#Exit(0)
