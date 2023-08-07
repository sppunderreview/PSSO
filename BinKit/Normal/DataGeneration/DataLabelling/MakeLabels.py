import pickle 

def reverseDict(dict):
    rd = {}    
    for charact in dict:        
        for idS in dict[charact]:
            rd[idS] = charact
    return rd
    
def addToDict(dict, charact, idS):
    if not(charact in dict):
        dict[charact] = []
    dict[charact] += [idS]
    
def listCharacs(dict):
    print([(x,len(dict[x])) for x in dict])

def collectQB(dict):
    QBs = []
    for x in dict:
        for y in dict:
            if x == y:
                continue
            n = x+"/"+y 
            QBs += [[n, dict[x], dict[y]]]
    return QBs

EMBEDS = ["BSIZE","DSIZE","FUNCTIONSET","LIBDX","MUTANTX","PSS","PSSO","ASCG","SHAPE","STRINGSET"]
with open("BSIZE", "rb") as f:
    IDS = set([idS for idS in pickle.load(f)])

for n in EMBEDS:
    with open(n, "rb") as f:
        O = set([idS for idS in pickle.load(f)])
        IDS = IDS.intersection(O)

Projets = {}
Compilers = {}
Archs = {}
Endians = {}
Optims = {}
Names = {}
 

for idS in IDS:
    t = idS.split("_")
    project   = t[0]
    compiler  = t[1]
    arch      = t[2]
    endianess = t[3]
    optim     = t[4] 
    nameProgram = project+"_"+"_".join(t[5:])
    addToDict(Projets, project, idS)
    addToDict(Compilers, compiler, idS)
    addToDict(Archs, arch, idS)
    addToDict(Endians, endianess, idS)
    addToDict(Optims, optim, idS)
    addToDict(Names, nameProgram, idS)

listCharacs(Projets)
listCharacs(Compilers)
listCharacs(Archs)
listCharacs(Endians)
listCharacs(Optims)
listCharacs(Names)


"""
[('libidn-2.0.5', 288), ('binutils-2.30', 4032), ('coreutils-8.29', 30239), ('dap-3.10', 1152), ('recutils-1.7', 2880), ('ccd2cue-0.5', 288), ('tar-1.30', 576), ('libiconv-1.15', 864), ('sharutils-4.15.2', 1152), ('wdiff-1.2.2', 288), ('lightning-2.1.2', 288), ('inetutils-1.9.4', 5184), ('enscript-1.6.6', 864), ('cppi-1.18', 288), ('libtasn1-4.13', 1152), ('gdbm-1.15', 1152), ('gsl-2.5', 1152), ('bool-0.2.2', 288), ('gcal-4.1', 1152), ('direvent-5.1', 288), ('patch-2.7.6', 288), ('findutils-4.6.0', 1728), ('plotutils-2.6', 864), ('libunistring-0.9.10', 288), ('libmicrohttpd-0.9.59', 288), ('nettle-3.4', 1152), ('hello-2.10', 288), ('osip-5.0.0', 576), ('libtool-2.4.6', 288), ('gawk-4.2.1', 288), ('datamash-1.3', 288), ('gnu-pw-mgr-2.3.1', 576), ('units-2.16', 288), ('gsasl-1.8.0', 288), ('macchanger-1.6.0', 288), ('a2ps-4.14', 576), ('which-2.21', 288), ('readline-7.0', 576), ('glpk-4.65', 576), ('gnudos-1.11.4', 576), ('gss-1.0.3', 576), ('gmp-6.1.2', 288), ('time-1.9', 288), ('cflow-1.5', 288), ('xorriso-1.4.8', 288), ('gzip-1.9', 288), ('cpio-2.12', 576), ('texinfo-6.5', 288), ('grep-3.1', 288), ('sed-4.5', 288), ('spell-1.1', 288)]
[('gcc-7.3.0', 7520), ('gcc-4.9.4', 7519), ('clang-5.0', 7520), ('clang-4.0', 7520), ('gcc-8.2.0', 7520), ('gcc-6.4.0', 7520), ('clang-7.0', 7520), ('clang-6.0', 7520), ('gcc-5.5.0', 7520)]
[('arm', 16920), ('mipseb', 16920), ('mips', 16919), ('x86', 16920)]
[('64', 33840), ('32', 33839)]
[('O2', 16919), ('O1', 16920), ('O0', 16920), ('O3', 16920)]
[('libidn-2.0.5_idn2.elf', 288), ('binutils-2.30_addr2line.elf', 288), ('binutils-2.30_as.elf', 288), ('coreutils-8.29_unexpand.elf', 288), ('binutils-2.30_ranlib.elf', 288), ('coreutils-8.29_stat.elf', 288), ('dap-3.10_dapruns.elf', 288), ('binutils-2.30_gprof.elf', 288), ('coreutils-8.29_shred.elf', 288), ('recutils-1.7_librec.so.1.0.0.elf', 288), ('coreutils-8.29_realpath.elf', 288), ('ccd2cue-0.5_ccd2cue.elf', 288), ('recutils-1.7_rec2csv.elf', 288), ('tar-1.30_tar.elf', 288), ('coreutils-8.29_dd.elf', 288), ('recutils-1.7_recsel.elf', 288), ('libiconv-1.15_libiconv.so.2.6.0.elf', 288), ('sharutils-4.15.2_uudecode.elf', 288), ('coreutils-8.29_ln.elf', 288), ('coreutils-8.29_comm.elf', 288), ('wdiff-1.2.2_wdiff.elf', 288), ('coreutils-8.29_dir.elf', 288), ('lightning-2.1.2_liblightning.so.1.0.0.elf', 288), ('inetutils-1.9.4_hostname.elf', 288), ('libiconv-1.15_libcharset.so.1.0.0.elf', 288), ('coreutils-8.29_ptx.elf', 288), ('binutils-2.30_objdump.elf', 288), ('coreutils-8.29_whoami.elf', 288), ('inetutils-1.9.4_uucpd.elf', 288), ('coreutils-8.29_rm.elf', 288), ('enscript-1.6.6_states.elf', 288), ('binutils-2.30_strip.elf', 288), ('cppi-1.18_cppi.elf', 288), ('coreutils-8.29_dirname.elf', 288), ('inetutils-1.9.4_whois.elf', 288), ('coreutils-8.29_touch.elf', 288), ('coreutils-8.29_tac.elf', 288), ('coreutils-8.29_cat.elf', 288), ('libtasn1-4.13_asn1Decoding.elf', 288), ('coreutils-8.29_truncate.elf', 288), ('coreutils-8.29_chroot.elf', 288), ('coreutils-8.29_runcon.elf', 288), ('inetutils-1.9.4_dnsdomainname.elf', 288), ('gdbm-1.15_gdbmtool.elf', 288), ('gsl-2.5_gsl-histogram.elf', 288), ('inetutils-1.9.4_rshd.elf', 288), ('bool-0.2.2_bool.elf', 288), ('coreutils-8.29_expr.elf', 288), ('gcal-4.1_gcal2txt.elf', 288), ('inetutils-1.9.4_rexecd.elf', 288), ('direvent-5.1_direvent.elf', 288), ('inetutils-1.9.4_tftpd.elf', 288), ('coreutils-8.29_du.elf', 288), ('patch-2.7.6_patch.elf', 288), ('coreutils-8.29_df.elf', 288), ('recutils-1.7_recfmt.elf', 288), ('findutils-4.6.0_code.elf', 288), ('gcal-4.1_tcal.elf', 288), ('recutils-1.7_recset.elf', 288), ('coreutils-8.29_chmod.elf', 288), ('plotutils-2.6_double.elf', 288), ('libunistring-0.9.10_libunistring.so.2.1.0.elf', 288), ('coreutils-8.29_true.elf', 288), ('coreutils-8.29_mknod.elf', 288), ('coreutils-8.29_tsort.elf', 288), ('coreutils-8.29_vdir.elf', 288), ('coreutils-8.29_hostid.elf', 288), ('coreutils-8.29_timeout.elf', 288), ('coreutils-8.29_join.elf', 288), ('sharutils-4.15.2_shar.elf', 288), ('coreutils-8.29_nice.elf', 288), ('coreutils-8.29_unlink.elf', 288), ('coreutils-8.29_stdbuf.elf', 288), ('libmicrohttpd-0.9.59_libmicrohttpd.so.12.46.0.elf', 288), ('enscript-1.6.6_enscript.elf', 288), ('inetutils-1.9.4_inetd.elf', 288), ('recutils-1.7_recdel.elf', 288), ('inetutils-1.9.4_telnet.elf', 288), ('binutils-2.30_ar.elf', 288), ('recutils-1.7_recfix.elf', 288), ('coreutils-8.29_cut.elf', 288), ('coreutils-8.29_fold.elf', 288), ('coreutils-8.29_wc.elf', 288), ('nettle-3.4_nettle-lfib-stream.elf', 288), ('coreutils-8.29_shuf.elf', 288), ('hello-2.10_hello.elf', 288), ('dap-3.10_daprun.elf', 288), ('coreutils-8.29_basename.elf', 288), ('coreutils-8.29_pwd.elf', 288), ('inetutils-1.9.4_rexec.elf', 288), ('coreutils-8.29_mv.elf', 288), ('osip-5.0.0_libosipparser2.so.12.0.0.elf', 288), ('coreutils-8.29_base32.elf', 288), ('coreutils-8.29_false.elf', 288), ('coreutils-8.29_uname.elf', 288), ('gdbm-1.15_gdbm_dump.elf', 288), ('coreutils-8.29_expand.elf', 288), ('coreutils-8.29_dircolors.elf', 288), ('coreutils-8.29_sleep.elf', 288), ('inetutils-1.9.4_rlogind.elf', 288), ('binutils-2.30_nm.elf', 288), ('coreutils-8.29_[.elf', 288), ('coreutils-8.29_printenv.elf', 288), ('libtool-2.4.6_libltdl.so.7.3.1.elf', 288), ('gawk-4.2.1_gawk.elf', 288), ('datamash-1.3_datamash.elf', 288), ('recutils-1.7_recins.elf', 288), ('coreutils-8.29_numfmt.elf', 288), ('coreutils-8.29_pr.elf', 288), ('findutils-4.6.0_bigram.elf', 288), ('gsl-2.5_libgsl.so.23.1.0.elf', 288), ('coreutils-8.29_chgrp.elf', 287), ('binutils-2.30_c++filt.elf', 288), ('coreutils-8.29_seq.elf', 288), ('gnu-pw-mgr-2.3.1_gnu-pw-mgr.elf', 288), ('binutils-2.30_elfedit.elf', 288), ('nettle-3.4_nettle-hash.elf', 288), ('coreutils-8.29_pinky.elf', 288), ('binutils-2.30_objcopy.elf', 288), ('units-2.16_units.elf', 288), ('coreutils-8.29_stty.elf', 288), ('coreutils-8.29_echo.elf', 288), ('coreutils-8.29_sort.elf', 288), ('gsasl-1.8.0_libgsasl.so.7.9.6.elf', 288), ('coreutils-8.29_date.elf', 288), ('gsl-2.5_libgslcblas.so.0.0.0.elf', 288), ('inetutils-1.9.4_ftpd.elf', 288), ('macchanger-1.6.0_macchanger.elf', 288), ('dap-3.10_dap.elf', 288), ('gnu-pw-mgr-2.3.1_sort-pw-cfg.elf', 288), ('a2ps-4.14_a2ps.elf', 288), ('inetutils-1.9.4_logger.elf', 288), ('coreutils-8.29_tee.elf', 288), ('sharutils-4.15.2_uuencode.elf', 288), ('which-2.21_which.elf', 288), ('readline-7.0_libhistory.so.7.0.elf', 288), ('binutils-2.30_size.elf', 288), ('coreutils-8.29_cp.elf', 288), ('glpk-4.65_libglpk.so.40.3.0.elf', 288), ('coreutils-8.29_chown.elf', 288), ('plotutils-2.6_spline.elf', 288), ('findutils-4.6.0_frcode.elf', 288), ('coreutils-8.29_logname.elf', 288), ('libtasn1-4.13_asn1Parser.elf', 288), ('coreutils-8.29_sha224sum.elf', 288), ('coreutils-8.29_md5sum.elf', 288), ('coreutils-8.29_sha384sum.elf', 288), ('coreutils-8.29_mkfifo.elf', 288), ('coreutils-8.29_factor.elf', 288), ('coreutils-8.29_split.elf', 288), ('coreutils-8.29_libstdbuf.so.elf', 288), ('gnudos-1.11.4_prime.elf', 288), ('coreutils-8.29_sha1sum.elf', 288), ('gss-1.0.3_gss.elf', 288), ('enscript-1.6.6_mkafmmap.elf', 288), ('coreutils-8.29_fmt.elf', 288), ('coreutils-8.29_groups.elf', 288), ('gmp-6.1.2_libgmp.so.10.3.2.elf', 288), ('coreutils-8.29_install.elf', 288), ('coreutils-8.29_nl.elf', 288), ('time-1.9_time.elf', 288), ('coreutils-8.29_id.elf', 288), ('cflow-1.5_cflow.elf', 288), ('coreutils-8.29_pathchk.elf', 288), ('xorriso-1.4.8_xorriso.elf', 288), ('coreutils-8.29_sync.elf', 288), ('inetutils-1.9.4_ftp.elf', 288), ('coreutils-8.29_tail.elf', 288), ('coreutils-8.29_mktemp.elf', 288), ('coreutils-8.29_users.elf', 288), ('gzip-1.9_gzip.elf', 288), ('gsl-2.5_gsl-randist.elf', 288), ('coreutils-8.29_b2sum.elf', 288), ('gnudos-1.11.4_mino.elf', 288), ('osip-5.0.0_libosip2.so.12.0.0.elf', 288), ('coreutils-8.29_sha512sum.elf', 288), ('libtasn1-4.13_libtasn1.so.6.5.5.elf', 288), ('coreutils-8.29_mkdir.elf', 288), ('coreutils-8.29_who.elf', 288), ('cpio-2.12_cpio.elf', 288), ('nettle-3.4_sexp-conv.elf', 288), ('readline-7.0_libreadline.so.7.0.elf', 288), ('plotutils-2.6_ode.elf', 288), ('texinfo-6.5_install-info.elf', 288), ('coreutils-8.29_od.elf', 288), ('coreutils-8.29_tty.elf', 288), ('coreutils-8.29_uniq.elf', 288), ('coreutils-8.29_yes.elf', 288), ('coreutils-8.29_chcon.elf', 288), ('libiconv-1.15_iconv.elf', 288), ('coreutils-8.29_printf.elf', 288), ('coreutils-8.29_csplit.elf', 288), ('coreutils-8.29_nohup.elf', 288), ('coreutils-8.29_head.elf', 288), ('coreutils-8.29_env.elf', 288), ('coreutils-8.29_base64.elf', 288), ('dap-3.10_dappp.elf', 288), ('recutils-1.7_recinf.elf', 288), ('sharutils-4.15.2_unshar.elf', 288), ('gcal-4.1_gcal.elf', 288), ('cpio-2.12_rmt.elf', 288), ('coreutils-8.29_sum.elf', 288), ('coreutils-8.29_paste.elf', 288), ('gdbm-1.15_gdbm_load.elf', 288), ('coreutils-8.29_ls.elf', 288), ('findutils-4.6.0_xargs.elf', 288), ('coreutils-8.29_readlink.elf', 288), ('binutils-2.30_readelf.elf', 288), ('inetutils-1.9.4_telnetd.elf', 288), ('a2ps-4.14_fixnt.elf', 288), ('nettle-3.4_nettle-pbkdf2.elf', 288), ('coreutils-8.29_nproc.elf', 288), ('coreutils-8.29_kill.elf', 288), ('grep-3.1_grep.elf', 288), ('findutils-4.6.0_find.elf', 288), ('glpk-4.65_glpsol.elf', 288), ('coreutils-8.29_tr.elf', 288), ('sed-4.5_sed.elf', 288), ('recutils-1.7_csv2rec.elf', 288), ('findutils-4.6.0_locate.elf', 288), ('inetutils-1.9.4_talkd.elf', 288), ('inetutils-1.9.4_syslogd.elf', 288), ('binutils-2.30_strings.elf', 288), ('coreutils-8.29_cksum.elf', 288), ('coreutils-8.29_rmdir.elf', 288), ('gss-1.0.3_libgss.so.3.0.3.elf', 288), ('spell-1.1_spell.elf', 288), ('inetutils-1.9.4_tftp.elf', 288), ('gcal-4.1_txt2gcal.elf', 288), ('gdbm-1.15_libgdbm.so.6.0.0.elf', 288), ('libtasn1-4.13_asn1Coding.elf', 288), ('coreutils-8.29_sha256sum.elf', 288), ('coreutils-8.29_link.elf', 288), ('coreutils-8.29_uptime.elf', 288), ('tar-1.30_rmt.elf', 288)]
"""

T = reverseDict(Names)
QBs = collectQB(Compilers) + collectQB(Archs) + collectQB(Endians) + collectQB(Optims)
"""
[('clang-7.0/gcc-6.4.0', 7520, 7520), ('clang-7.0/gcc-7.3.0', 7520, 7520), ('clang-7.0/clang-5.0', 7520, 7520), ('clang-7.0/gcc-5.5.0', 7520, 7520), ('clang-7.0/clang-6.0', 7520, 7520), ('clang-7.0/gcc-8.2.0', 7520, 7520), ('clang-7.0/gcc-4.9.4', 7520, 7519), ('clang-7.0/clang-4.0', 7520, 7520), ('gcc-6.4.0/clang-7.0', 7520, 7520), ('gcc-6.4.0/gcc-7.3.0', 7520, 7520), ('gcc-6.4.0/clang-5.0', 7520, 7520), ('gcc-6.4.0/gcc-5.5.0', 7520, 7520), ('gcc-6.4.0/clang-6.0', 7520, 7520), ('gcc-6.4.0/gcc-8.2.0', 7520, 7520), ('gcc-6.4.0/gcc-4.9.4', 7520, 7519), ('gcc-6.4.0/clang-4.0', 7520, 7520), ('gcc-7.3.0/clang-7.0', 7520, 7520), ('gcc-7.3.0/gcc-6.4.0', 7520, 7520), ('gcc-7.3.0/clang-5.0', 7520, 7520), ('gcc-7.3.0/gcc-5.5.0', 7520, 7520), ('gcc-7.3.0/clang-6.0', 7520, 7520), ('gcc-7.3.0/gcc-8.2.0', 7520, 7520), ('gcc-7.3.0/gcc-4.9.4', 7520, 7519), ('gcc-7.3.0/clang-4.0', 7520, 7520), ('clang-5.0/clang-7.0', 7520, 7520), ('clang-5.0/gcc-6.4.0', 7520, 7520), ('clang-5.0/gcc-7.3.0', 7520, 7520), ('clang-5.0/gcc-5.5.0', 7520, 7520), ('clang-5.0/clang-6.0', 7520, 7520), ('clang-5.0/gcc-8.2.0', 7520, 7520), ('clang-5.0/gcc-4.9.4', 7520, 7519), ('clang-5.0/clang-4.0', 7520, 7520), ('gcc-5.5.0/clang-7.0', 7520, 7520), ('gcc-5.5.0/gcc-6.4.0', 7520, 7520), ('gcc-5.5.0/gcc-7.3.0', 7520, 7520), ('gcc-5.5.0/clang-5.0', 7520, 7520), ('gcc-5.5.0/clang-6.0', 7520, 7520), ('gcc-5.5.0/gcc-8.2.0', 7520, 7520), ('gcc-5.5.0/gcc-4.9.4', 7520, 7519), ('gcc-5.5.0/clang-4.0', 7520, 7520), ('clang-6.0/clang-7.0', 7520, 7520), ('clang-6.0/gcc-6.4.0', 7520, 7520), ('clang-6.0/gcc-7.3.0', 7520, 7520), ('clang-6.0/clang-5.0', 7520, 7520), ('clang-6.0/gcc-5.5.0', 7520, 7520), ('clang-6.0/gcc-8.2.0', 7520, 7520), ('clang-6.0/gcc-4.9.4', 7520, 7519), ('clang-6.0/clang-4.0', 7520, 7520), ('gcc-8.2.0/clang-7.0', 7520, 7520), ('gcc-8.2.0/gcc-6.4.0', 7520, 7520), ('gcc-8.2.0/gcc-7.3.0', 7520, 7520), ('gcc-8.2.0/clang-5.0', 7520, 7520), ('gcc-8.2.0/gcc-5.5.0', 7520, 7520), ('gcc-8.2.0/clang-6.0', 7520, 7520), ('gcc-8.2.0/gcc-4.9.4', 7520, 7519), ('gcc-8.2.0/clang-4.0', 7520, 7520), ('gcc-4.9.4/clang-7.0', 7519, 7520), ('gcc-4.9.4/gcc-6.4.0', 7519, 7520), ('gcc-4.9.4/gcc-7.3.0', 7519, 7520), ('gcc-4.9.4/clang-5.0', 7519, 7520), ('gcc-4.9.4/gcc-5.5.0', 7519, 7520), ('gcc-4.9.4/clang-6.0', 7519, 7520), ('gcc-4.9.4/gcc-8.2.0', 7519, 7520), ('gcc-4.9.4/clang-4.0', 7519, 7520), ('clang-4.0/clang-7.0', 7520, 7520), ('clang-4.0/gcc-6.4.0', 7520, 7520), ('clang-4.0/gcc-7.3.0', 7520, 7520), ('clang-4.0/clang-5.0', 7520, 7520), ('clang-4.0/gcc-5.5.0', 7520, 7520), ('clang-4.0/clang-6.0', 7520, 7520), ('clang-4.0/gcc-8.2.0', 7520, 7520), ('clang-4.0/gcc-4.9.4', 7520, 7519), ('x86/mipseb', 16920, 16920), ('x86/arm', 16920, 16920), ('x86/mips', 16920, 16919), ('mipseb/x86', 16920, 16920), ('mipseb/arm', 16920, 16920), ('mipseb/mips', 16920, 16919), ('arm/x86', 16920, 16920), ('arm/mipseb', 16920, 16920), ('arm/mips', 16920, 16919), ('mips/x86', 16919, 16920), ('mips/mipseb', 16919, 16920), ('mips/arm', 16919, 16920), ('64/32', 33840, 33839), ('32/64', 33839, 33840), ('O0/O3', 16920, 16920), ('O0/O2', 16920, 16919), ('O0/O1', 16920, 16920), ('O3/O0', 16920, 16920), ('O3/O2', 16920, 16919), ('O3/O1', 16920, 16920), ('O2/O0', 16919, 16920), ('O2/O3', 16919, 16920), ('O2/O1', 16919, 16920), ('O1/O0', 16920, 16920), ('O1/O3', 16920, 16920), ('O1/O2', 16920, 16919)]
"""


with open("T", "wb") as f:
    pickle.dump(T, f)

with open("QBs", "wb") as f:
    pickle.dump(QBs, f)



Metacompilers = {}
Metacompilers['gcc']   =   [y for x in ['gcc-6.4.0', 'gcc-7.3.0',  'gcc-5.5.0',  'gcc-8.2.0', 'gcc-4.9.4'] for y in Compilers[x]]
Metacompilers['clang'] =   [y for x in ['clang-7.0', 'clang-5.0',  'clang-6.0','clang-4.0'] for y in Compilers[x]]

listCharacs(Metacompilers)
# [('gcc', 37599), ('clang', 30080)]

QBAs = collectQB(Metacompilers)
with open("QBAs", "wb") as f:
    pickle.dump(QBAs, f)