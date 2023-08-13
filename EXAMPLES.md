# Examples

## PSSO on the Basic Dataset (8 minutes)

**Command:**
```bash
conda activate PSS_Base
python3 SetAbsolutePaths.py
cd PSSO/
python3 Preprocess.py 
```

**Output:**
```console
Reading .json
Program codeblocks with O1 , # of local CFG: 3642 , time: 1.3974053859710693 s
Program ssh with O2 , # of local CFG: 1622 , time: 0.5432868003845215 s
Program perl with O1 , # of local CFG: 2225 , time: 1.4496872425079346 s
Program openssl with O1 , # of local CFG: 3464 , time: 0.674699068069458 s
Program libgeany.so.0.0.0 with O2 , # of local CFG: 7653 , time: 2.8476717472076416 s
Program libgeany.so.0.0.0 with O1 , # of local CFG: 7209 , time: 2.7797937393188477 s
Program codeblocks with O0 , # of local CFG: 4430 , time: 1.8078033924102783 s
Program sort with O0 , # of local CFG: 368 , time: 0.1629476547241211 s
Program cp with O0 , # of local CFG: 391 , time: 0.09430146217346191 s
Program git with O0 , # of local CFG: 4065 , time: 1.414459228515625 s
Program openssl with O3 , # of local CFG: 3496 , time: 0.7026350498199463 s
Program ssh with O1 , # of local CFG: 1589 , time: 0.5069830417633057 s
Program libgeany.so.0.0.0 with O0 , # of local CFG: 14624 , time: 4.75564432144165 s
Program ruby with O1 , # of local CFG: 5700 , time: 2.687840461730957 s
Program cmp with O0 , # of local CFG: 149 , time: 0.1868577003479004 s
Program diff with O0 , # of local CFG: 365 , time: 0.0939018726348877 s
...
```

**Command:**
```bash
python3 RunMakeMD3.py
```
**Output:**
```console
Basic Subdataset BO
Computing similarity indices for Program codeblocks with O1
100%|| 84/84 [00:00<00:00, 11437.53it/s]
Computing similarity indices for Program ssh with O2
100%|███████████████████| 84/84 [00:00<00:00, 16027.00it/s]
Computing similarity indices for Program perl with O1
100%|███████████████████| 84/84 [00:00<00:00, 26028.48it/s]
Computing similarity indices for Program openssl with O1
100%|███████████████████| 84/84 [00:00<00:00, 32367.62it/s]
Computing similarity indices for Program libgeany.so.0.0.0 with O2
100%|████████████████████| 84/84 [00:00<00:00, 3396.85it/s]
Computing similarity indices for Program libgeany.so.0.0.0 with O1
100%|███████████████████| 84/84 [00:00<00:00, 39034.07it/s]
Computing similarity indices for Program codeblocks with O0
100%|███████████████████| 84/84 [00:00<00:00, 39864.40it/s]
Computing similarity indices for Program sort with O0
100%|███████████████████| 84/84 [00:00<00:00, 46382.51it/s]
Computing similarity indices for Program cp with O0
100%|███████████████████| 84/84 [00:00<00:00, 44727.88it/s]
...
```

**Command:**
```bash
python3 RunMakeMD.py 
```
**Output:**
```console
Basic Subdataset BO
Testfield O0 -> O1
100%|███████████████████| 21/21 [00:00<00:00, 44984.87it/s]
Testfield O0 <- O1
100%|| 21/21 [00:00<00:00, 125649.62it/s]
Testfield O0 <-> O1
100%|███████████████████| 42/42 [00:00<00:00, 65341.53it/s]
Basic Subdataset BO
Testfield O0 -> O2
100%|███████████████████| 21/21 [00:00<00:00, 144869.05it/s]
Testfield O0 <- O2
100%|███████████████████| 21/21 [00:00<00:00, 144631.17it/s]
Testfield O0 <-> O2
100%|███████████████████| 42/42 [00:00<00:00, 66076.81it/s]
Basic Subdataset BO
Testfield O0 -> O3
100%|███████████████████| 21/21 [00:00<00:00, 142294.64it/s]
Testfield O0 <- O3
100%|███████████████████| 21/21 [00:00<00:00, 90153.92it/s]
Testfield O0 <-> O3
100%|███████████████████| 42/42 [00:00<00:00, 38521.93it/s]
...
```

**Command:**
```bash
cd ../
python3 MakeTables.py
```

**Output:**
```console
Loading the Preliminary Evaluation Table ...
Table (Preliminary Evaluation) Total runtimes on the Basic dataset
               Total
...
PSSO          14m28s
...

Loading RQ1 Tables ...
Table (RQ1) Total runtimes.
Include preprocessing time.
Significant preprocessing times reported in "( )".
                       Basic   ...
...
PSSO         14m28s (14m24s)   ...
...

Table (RQ1) Runtimes per clone search (sec).
Include preprocessing time.
Significant preprocessing times reported in "( )".
                     Basic   ...
...
PSSO         0.26s (0.26s)   ...
...

Loading the RQ2 Table ...
Table (RQ2) Pecision Scores.
            Basic  ...
...
PSSO         0.38  ...
...

Table (RQ3) Average rank-biserial correlation for H on the Basic dataset.
                              CO              UO              BO         Average
...
PSSO               \textbf{0.12}   \textbf{0.09}  \textbf{-0.02}   \textbf{0.06}
...

...

All Tables generated in 101.98 s
```


## SAFE function embedding on the Coreutils Versions subdataset (8 minutes)

**Command:**
```bash
conda activate PSS_Base
python3 SetAbsolutePaths.py
cd SAFE/makeEmbeds
python3 computesEmbeddings.py
```
**Output:**
```console
Computing Coreutils Versions functions embeddings for each program! (5 minutes)
 100%|████████████████████| 348/348 [04:15<00:00,  1.36it/s]
```

**Command:**
```bash
python3 readEmbeddings.py
```

**Output:**
```console
\# of unique function names: 5083
Function: .init_proc
Inside 348 programs of Coreutils Versions
...
```

![Image of SAFE function embeddings for .init_proc from Coreutils Versions](./SAFE/makeEmbeds/init_proc_CV.png "Image of SAFE function embeddings for .init_proc from Coreutils Versions")

You can quit the bash terminal to end the visualization script.

## StringSet on a hundred IoT malwares (5 minutes)

**Command:**
```bash
conda activate PSS_Base
cd IoT/DataGeneration/STRINGSET/
python3 Preprocess.py
```
**Output:**
```console
IoT malware hash: 2a87e1c78db87d283f79adff2d5e4c29e085dd7e931fbb91326af22e8ef7ff0d.elf
String literals: ['n+A\t', 'ff/F/', '/sm"O,', 'w`;!', "qx'g", ' !3b', 'r ask', 's3kD', 'qsj !<', 'h+A\t', 'Lds`La', 'lfSa', 'a`12', 's#e04', 'RdH$', '"\\en', ',b#a', ',dQ@', '.xQlj', '+-qP', 'Ti @', '(}DL', 'b\tr3', 'd"qzU', '(wr/', 'a{";', '@;":', ")'#a)#", 'AmB{!+#;!', '^]cla\\', 'APe|l3j', "tP'(x", ')q (', 'F*xM', '(,qp!', 'a{"A', '@;"@', 'c^|c,a', 'ahP\\b', 'F*xK', '/"O{', 'qb`cb', ' ch@', '&\ttpgc`', '"ca!# ', ' !cb', '-b|1', 'h{"&', '@;"%', "P)'#a)#", '/"Og', 'AmH|g;"\'', '"}@$', "2)'#a)#)A", 'Q]cln\\', 'F*xH', '|33a', 'k#-@', '62/a', '6"QnS', 'R#ay!p1', '|?&O', ")'#a)#)A", 'Q{#+#y', '9"3a', 'c,ai ', 'c#g#a', '*"aqc', 'x1("Q', '#)!r', 'W)!o', 'V)!\t', '2*Uk!g', 'd)!d', '`)!a', 'Q(ve', 's#3?', '7zPz](p', '@ 5@', '-a@a', '2-a#`)@', '/s`miCWDX', "\tt@bsa9'", '`)A|1)@,b9(', '3b) ', 'h!d!`!\\!X!T!P!L!H!x!t!p!l!4!`', 'c|sSd', 's0!,!(!$! !', '!D!@!<!8!', 'd!|!`!\\!X!T!\t', 'tP!|!L!H!x!t!p!\t', 'tl!|!4!0!,!(!\t', 't$!|! !', 'D!|!@!<!8!', 'P0al', '!|!\t', 'JseZ', 'J3eZ', '7|2"a', '(33a', 'mfla', '#a}A', '"Bc#`ra', '&Ra2%', 'Gz#:"* ', 'a3g-G', 'f*!2-z#', 'Az"j!#c', 'C*#2$', 'ech3fsb', 'ccsb', '"ca:!#c', 'C*#1$', 'b+2!', 'Cb+z":&#aj"R*', '/"OAP', '/"O;', 'P,1&', 'g3amA|1Qf', 'ql22,!!!%', 'sf\\1', 'A+!x', '$cPq&', 'HCe1', 'HCe.', 'HCe}', 'HCex', 'HCeu', 'HCes', ')\tH$', '3`D%', "x'3``", '3`~$T', "3`x'", '#`3`', '#`3`#', '2Uq)', '3^q)', "m<!x'", '8#pq', 'mf"h', '@qs`', "x'3`?", '#`3`^', ' #`J', '#`3`G', 'B<cmA{"o', '#;"$', 'DRrd', '21"^', '#bdw', "3a9'", 'V9")A', 'A;"-', '{!+!-', "GMA;'", '"+\'`7', 'Cc,3Sf', 'x`8S', '3d3Q', 'a(1f1', 'XsamA', 'C;""!', 'T3a-A', 'A3`L1', 'G{""!', ')#;a', 'fAc$', 'H3eZ', '!a#e', 'VBa,6f', 'b,ap1', 'wl1v1', ' (pa', 'r f/', 'C#e\\', 'HlfF', ' qC`', 'Sb)BSa', 'ASc)C', 'h.d^cba|1', 'b:" !ba|1', '" !ba|1', 'wJ" !', 'J!!p', 'J!.0', 'r#`\\', '/"Ota', '4lb#a', 'r,aV11', 'ca81', 'r#`L', 'S`#q', ' !Cc', 'b|2 a', 'CcKc8#', '%ZE-', 'q)!h', '(w2"$qq', 'wraSc', '@~3`', ' 3`@~', 'q"f3`', ' @~3`', '/3`"O', 'wra6', '/Sh"O', '3e3a u', 'a,q3b2', '0R!S', 'emf3`', '/"OB`', '/"O+', '/Ci"O', '28#!', 'uCb^', 'sc&0(C', 'sc&0', 'c`K [ h&', 'C`l0', 'H5g1', 'Scg1', 'uCg^', 'w(&Sc', '#Cb00', 'qQSRVSWTXUYVZW[', '(!Sc', 'v0f ', 'qVcVf(@Vg= Vhm#Vi}&Vj', '#`K`cm', '&6DT', 'v3a;', 'v3a(', 'vra2"qS', 'vwSh&', ' r2"T', 'c {!', 'zcd&', 'u#dc`', 'bCa-GSP', '6Sil4', '#`C`', '!\tB".', '*:JZ', 'rCa!W', 'rCa"V', 'rCa#W', 'rCa$V', 'rCa%W', 'rCa&V', "r'WCa\t", 'cCa(V', "s'Wg", 's"f8#r!', '"Cc {', 'j"UCc!X', 'j#WCc"U', 'rCc$V#W', 'j%XCc$V', 'Fca{!', 'ncg/', 'Cb\\fca', 'ca2"1', '\tA2"', '\t\'P"', 'C`X0', 'nCbTa', 'nB.Q', 'E"O\t', '/"OD', "'b)!", "h)('", '/ScG', '/"OT', 'h+B\t', '#a,q', '3b"$', '3b(1', ' 80"%', 'n"c81', "!Wx'", '"Q!R', 'c!R("', '/h&b', "x'R$x'", '"OBh', 'l98#', 'e2a2V', 'sarb(1', ',93fsesh', '/"O_', 'A|11', 'p"OSS', 'nRR8##f', 'eQQ(1!A!A', '2<2/', "!C'9", 'A<1#c', 'A8#,13', 'Race', '#cL33d', 'gfff', 'BcAR2a3f&g', 'vFU|1', '/"OSR', 'nH$RW', '("B\'2', '4G:*2', '4B#S6', '|2")', '1!A!A', '/"OF', '8"O!H', '/l5"O', 'pScS', '2("!ba', 'CmR(O', 'Sb&a', 'c@s7P', '=R;Q 1\t', '!H"!', 'da)mf0a', '/"Ol', '#<7&7', '/Sf"O', 'b0Q r', '(-b2Qq', 'Q-b"(]e', '1a-b', 't@b#`', '("#`.', 'sc-Cy!sb', 'G)B|g', '"{#;""*', '/Ck"O;', 'R|q3', '*@l?', '37.0.10.182', '0125!8 ', "58 '8%", ',<8#', '#$6;b', '&;; ', ',7gaae', '"=.,"', '?8"efg', '509=:', '.-50efg`', '.8,,z', '?;d"=.,"', '?;d509=:', '<=gael', '75 edfm', '5::=1fdef', '7<5:3191', "3!1' ", 'efg`a.', 'efg`ab', "!'1&", "$5''", "$5''#;&0", '509=:efg`', "'!$$;& ", '93gadd', '91&8=:', '0519;:', '!6: ', 'pkkv', 'vkkp', "'<188T", '1:5681T', "'-' 19T", "{6=:{6!'-6;,t", 'nt5$$81 t:; t2;!:0T', ':7;&&17 T', "{6=:{6!'-6;,t$'T", "{6=:{6!'-6;,t?=88tymtT", '{$&;7{T', '{1,1T', '{20T', "{95$'T", '{$&;7{:1 { 7$T', "{' 5 !'T", 'z5:=91T', '{$&;7{:1 {&;! 1T', "5''#;&0T", '{1 7{&1\';8"z7;:2T', ':591\'1&"1&tT', '{01"{#5 7<0;3T', '{01"{9=\'7{#5 7<0;3T', '$662*7!E', ';3=:T', '1: 1&T', 'e365`70;9ag:<$ef1=d?2>T', 'FTPjGNRGP"', 'lKeeGp', 'qMPCnmcfgp"', 'lKeeGpF', 'wkw"', 'kW{EWHGkSL"', 'AAcf"', 'RPMA', 'PMWVG"', 'ARWKLDM"', '`memokrq"', 'NMACN"', 'IHD"', 'UCVAJFME"', 'OKQA', 'dvufv', '}UCVAJFME"', 'LGVQNKLI', 'rpktoqe"', 'egvnmacnkr"', 'iknncvvi"', 'gCVQ', 'mDHjx', 'eJMQVuWXjGPG', 'uQec', 'caf`"', 'c@cF"', 'KCeT"', 'rmqv', 'UCLKRAL', 'ZON"', 'RKAFGQA', 'AVPNV', 'jlcr', 'NMEKL', 'AEK"', 'VOwL@NMAI', 'eRMLdMPO', 'KLFGZ', 'RJR"', 'QJGNN"', ';::17 10t', ';!&71t', ':3=:1t', '!1&-T', '/dev/null', 'CAk[S', '.shstrtab', '.init', '.text', '.fini', '.rodata', '.ctors', '.dtors', '.data', '.bss', '']
...
IoT malware hash: 1ec7746b189bfda654c2290033c25ab4c618abbee63a1bac7926b45f2f19d601.elf
String literals: ['TUPX!$', '3:?`3', '$? X', 's;g_', "/'hKY", 'mkR s', 's"1fo>', 'c{SO', 'K04p', 'OP`&', 'w[C@-', '2m{/', 'lc$ [w', "|kO'd*", 'PsO+~V', '7:?p', '_w`DPa', 'w}h1', 'H6c5', '?X/L ', ';BO#', "#{?'", 'Wu[~', '5_;?', ';oKD8', '-k+W', ' _S\t$2', "'{/#", "7'Q,CK70", 'eokR', '}g M', '4S*Cg', "t'P/", '0gws[', "'84A", '7\tSC|', 's":O3`!k', 'c`l{', 'jtga', ' anO', '`c3*H', '4SRgk', ']W1]', ',>m{0', "Sr#E[s'", 'R@dR', 'tgCF', '@fOl', 'p[tcz', 'p\\H`', '<P)wC@`', '3TP/', 'dksHC', ';&PC[', 'XTws', '~7l0Z', 'p?&`n', 'cqbJ', 'cc,,\t', 'i nQ/', '0 fP', '{9@(f\\', ';s,p,@', '`@$0bx', '\tc:,A#N', 'T$rp\\', 'W%\\s', '!3#Ck', '\tTpWq', 'U;cK', 'O,0/', '"weF', 'JZ/+', "%ln'", 'K\\4[R', 'SKVg', '76L ~R', '+C{I@', 'M`P40F[r', 'WJR**', '`\t[b', '+2W)', 'WC0.0', "x;'Z?%\\lA", 'Wd1n', '*0k^', '*4S3t ', 'KK#@(', 'u@6/', "+/'D", "'h?g+'%W", '${<;j+', 'W6(/', "!'0 3", ';,{<', 'cXgo', '_0_E', 'XC`"', 'p%rH', '8`3._', '8$ 3+', '@C7G', 'oMP tg', 'q|@l', '{Vw`8', 'IYr[', '.|J,";', 'B+3p', 'k+T3', '+G[@/{', ';Z?)3A', ']?(u', '+g{.u', 'SpP`', '  0!S[5', ' Ps{C', '",o(', '2{G{', "'g;`", '+",Y', '? :ST&', ':\tA3', ';XEK', '$Ce ', ' $2 D2E', '$C! ', '#$2#D9', "'Hd'", 'gX_{', '3@db', 'g*$2*', '-Hd-', 'C/$2/', 'Ch$61gC1$r', '*WcE0"', '>s]C', '0@6+', '"iw39495.2N', 'E;[caX', 'c_p 2`', 'S[cW.>', '; %sl', 'N\\!] ', '03fO', 'U"{6', "V#'[t3", "K's/oe", 'c/,7', 'k|+hv', 'V>XV', '+xdU', '\t"Sp', '{nH_', 'CS50', '{O]S', '-G;{', 'cTg`', 'l/!Uf', 'Sk$3', 'K(?s@', "'Hp5", '`,gH', 'M4<4H', ',4i@', 'Tdip', 'M$,5h', '7@-cA', 'OA k', 'K37DM_', 'C:$!', '3XMh', 'ht 7x?H', '3@K@}4', 'CDtS', '3^DW', 'tusp', '__h4d', '7|CH', '[CP`W', 'MG, 3LH', "*'4f", '@Wc>', 'uoq4', '#N0{s', '7[@i', '+kko', ',t{(', 'K!t?X', '3-Z\t', 'ioR!t', '_$!3', ' 3\\H', '%a#)', '_+|i', 'BHf |', '984?', 'lis=', '3xi^!H', "]F'* ", 'c3p 2r', 'k:/s', 'a.ii', '{e/c', '3DHt', 'o 2v', 'M$N ', 'C=Xo', ']Hfl', '{=@/', ';MN.0C', 't;/D', '?o3L1c', 'S|/r,', 'oGO"', 'EDt?', 'Wxc!Sz', 'w,+b0GXg', 's?CkCP}', " a+7'", '{pp_h', 'G[LG', 'HO2M', 'Rp%C', 'SK)7', '+k{U', "'3k'", 't+!Fg', '!Ljc', ' 9c0#', 'oQXG/', '#QR_', '#(+>k', 'gs<H', 'y6dh', "''<5", 'Qs`M', 'i{#O', '+m5\t', 'o#tO', 'sssH', '!wu#', "ww'_", '4S 3', 'MS  ', ' H02', "L'; .(RO", ':0RO', 'y`dX', 'x#i+', 'PC9<!}', '?n_9', '?#ep', 'CM 20', '#:stA', 'E #s', '7h|#P', '<MHP4X', '`Mhx4', 'L\\id', 'Cg^?', '-495', ':+W)', ';Akp', 'kaUk\\', '5#on', '5?$3', '_83*X', '<[60+', '#cw3', "'7? ", '6?`B', 'A|G"%\'', '7mV5', ';<C+jG', 'G<3?', 'KlGe P^;', 'KG!`', 'Sg{Ua?B', 'bP_`3', '`7b@', "\\w a'", 'I;.L@O', '<q.<1', 'mpcj/', 'MK(;', 'C4-8', '4w!;', 'p[@?', 'w6Od', '<=6U', '(`]g', 'vK08', 'RmCd', '`QH]', "h,g'/", 'QvOO?', '47,N', 'to$:', 'U/8[', 'j74A', 'pkvK', ' p? ', 'z{&?bG', 'HAB7', 'Lp{h', '?4#B;*C', '>)6om$N', ';,Ck', 'kS[G', ':++1|', '*Es#', '8+CG', '#1EmG', '[3m\\', 'SOH0', ",N'\t", 's?.O', "w'0p", "':oPa", '~Op1J', ',1 E', '"lp0%', ';2({&K', 'lL[*eKT', '8a/r', '}gZXk', 'p?]+', '_!gu', '_,*>w', '+Rv7', ')KD7s00', ';[KBS', 's_+n', '&kJ!', 'ho`GUbG', '/E|On;k', 'hs^\t', 'G?ScM', '2ST#m', '){Pp', '+/{[', 'H3AG', 'SE\\W&', '{{CDG', 'Dr#C', ';COcC', '#\tKXt?~w', '{ P;', '6S,a,', "+\tC'", 'U2;V', 'L"%y "4', '}WP>', "'G?Z [", '!r/vg', '/:_0/', '@,2H+s', 'PFGG', 'K^K(W', "1T'sO", ']3pL', ',c6W', 'O[Z/', 'l35;', 'CcWN', 'TGnc', '6cJ!', '+KzU)W', 'z(p``F', 'A0i/', 'loHnk', 'jiif', 'cbia', '[ZiY', 'WViU', 'SRiQ', 'ONiM', 'KJiI', 'GFiE', 'CBiA', '?>i=', ';:i9', '76i5', '32i1', '/.i-', '+*i)', "'&i%", '#"i!', '!m#*', 'ktWd', 'pR#?', 'G40;', 's^@B4', 'G_9{', 'xw![', 'H[ (', '0`KS', 'kODC{', 'oP`# ', 'AFj7', 'xc*p', '@wW12', 'AR7H', 'dl~@^', '\\&"m\'CA', 'IWv$', 'd0Ep', "T[D&'", "J_''", '/%V,', 'RCb#', 'UMwduc@', 'pbW2', '94!U', '[ch .cE', '[2Pqx', 'xW,[v', 'wP!"', "Cf_%'a#", '`md@', 'P0@n', 'P#f0', '.@`[D3', '-KA#', '@]8#450', '!wCC!', '"A7z', 'Gw=O', 'g"%~', 'P 2T', '4W+<GSk<', 'o`0`', '{8sp{', ', 0[', 'A!W/H', 'jk*6[', 'sb(u', 'tK<S', '6/O*', ' QCg<K-', 'vPo`/', 'P~LZ', '<P`3', '?#7n', '3r\t`', 'w;/Q', '0?Z7', '/CjOM', "\tOe,a'", 'vr+<gGGA.', '@sO[#a3', '[ {o', 'OTHc/k', 's$>k', '1T2Oz', 'WGA|', ' PFg7', '43< -', 'G/b@@', '{4w/', '#g |', 'a{[W)', 'wR7;0F', 't[S=;', '4wW+', '-3H#', 'kzKt', '*B?9`&', '.7S*', '\\/"W;', 'qh/\tC', 'w@g*lo01', "k#'p", "oS'5w", '!4EB', '(qwC/U', '$D &', '8HiH', 'Sn+1', 'K3Gl', '\\R>;', 'XHiH d', '\\TiL', 'FW.C', '{6CU', 'k;0G', 'n7X0D', '=_-u', '8oXA', 'PCcGo', 't+SO*o', 'L\t(;g', '<gP{', '!u/3', '1CPfO', 'g[l8', 'UH_"', 'r\t08', "G8[^'", 'cBDK', '.8Hd', 'h dw', 'q rv', "#Sv'", ';Q3kS', "R_,'7", 'OHZl', 'wD\\s', 'G7g^', 'a#I#', '\tcnU', '0wb ', 'm`VO', 'o!3K', '5{,3', '71_5', '&k /', '(awL', ' jDg', '+/+z#', 'b!k5c3`', '0D@u', '@lWC', 'nG|;', 'xsPkK', 'U\\W>', '#5ArO', ']\\e_', 'Yk4HV#', "!b/'", 'qW=G', 'H?}k', '5E+c+A', 'Q^O(v', '$3SU', 'NK(-', 'Cy?2', 'CX0m', 'TNC6', "D';3;", 'G83S', '[=C!C', '#Gu ', 'kSo8', "\\B'vv", 'KS\tc', '{0Tu', '4;HD', 'FSCP', 'OST /cdn', '-cgi7l HT', 'TP/1.1', 'User-Age', '0{GET', 'url=', '3ID5A', 'ATLINE O', 'N TOP', 'fghijklm', 'nopqr', 'uvw0', '12345678', '#SRQ', 'VB[C/1SZ^', 'VRZX', 'EXXC', 'A^MOAu', 'vT_:?', '7qOTn', 'BRD{k', "/D'{GXE", 'C3mZ', '\\zD^k', 'BDRE', 'OZ_S^', 'l+{J', '=DZT', 'RCb-7', 'tevq', 'gredx', 'qpb7&g', '[X@1', 'BV@R', 'XZp/', 'CyrG', 'VT\\Sy', 'k}TD', 'DU|G_', 'orDD@mFS', 'GRGV1', '`~t|', 'vYTl', 'mT=l', 'GSkV', '7-`s', 'PCx.', 'EVYD', 'hi^D\\RS', 'Tn|BS5', 'Y5FO"', '/{^AR-v', 'cNG as;', '@}EZ1', '\tt g-', 'fBlJNbG', 'y^ppRe', 'R~FY,', '^>iR', 'oVk~', '@EPY', '[:MD', "9Ol'O5", 'ZNC_', "%$'c]avS", 'uMdO{', '^g_X', '|^4M', '+a!V', '_UF:', 'dzvec', 'dy+#', '{m~@PvZm', 'Acp}', '~ao6', 'V{xh', 'Du_x', 'S45K', '(nil)', 'lLjztq', 'ifFeEgGa', 'ACScs', " +0-#'", 'I{tnko', 'error ', 'uesn"Op', 'atiok', 'qmit', '"h f', 'pkHA', 'vicV1a', 'Argum', ' liA', 'mxtk', "'vmaB", 'ynrcu', 'ly unav', '[KF~', 'ecmG-', 'Gaa/', '0inA', '5Ilm', 'eek|', '^fmo2k. ,:bVh', '&i5/', '|bmu.a', 'GIU4j,', ' 2~se', 'iz4g', 'mP>m', 'vod1Wc`', 'mTJ3', '[Amwl', 'k<in', 's3)s', 'tFc\t', "dL'c", '^-}Nb', 'Pg!4', 'KalB', '>~by', 'WwS=', '2Dwwr', '4mo|s>q@', 'ya#-Cs', 'azWN', ';U2)X', '=I/O ', '4*\\hOu', 'or:\t', ',ywX', 'd/o{`0r', '$Info: This file is packed with the UPX executable packer http://upx.sf.net $', '$Id: UPX 3.96 Copyright (C) 1996-2020 the UPX Team. All Rights Reserved. $', '/proc/self/exe', '{{ p', 'proc/sel', 'f/exe\\n', "-76'", 'm0gpk', '\\6;>', 'Q{{_', '+]6K', ';CUP', '1lWT(', 'M@4_', '"Sl1', "L+=ko'", "g'O,", 'K[nWS', 'v74`', 'kPX4:', 'GCC: (G', 'NU) 3.', '2 200', 'ian pre', 'leas', 'KDJv', '_Unwind_', 'VRS_Get', '~Compl', 'ception', 'Text', '~DataC', '>For', '=ais', '\tthrow', '_Pop', 'cpp_', '2}N)', 'guage', 'Specific', 'SHtrt', '/ho<', '8nal', 'build/', 'gcc-c', 'ib1f', 'xcs.[', '| AS ', '7.5.K', '1`ZE', '754-df.Sa', '.g-[', '{<6H', ')=p,', '*_sH', 'GX(d.HXO', '`w\\N', 'Zb r', 'ps0#Hk', "~`'n", 'pvrs', '_rtcv', '5!GU', '%exc', 'l/)bwV*+', '\to5,', '{$kgH} ', 'wD7id', '8T4`', 'zW5 ?', ';V99B', 'ic7c', 'cwe\t~', '$q6?', '=uw7W', '[<D-', '7lenY', 'F!nB', 'P7l|', 'rq&H', "p)E'", 'X r6', 'RE2$', '+:,:', '3nFd', '#NBr7p', 's)ZO', ']df:xY>', '\'"`\'l%', "K&esl'", '+X1i', 'C^-4', '8`>a', 'k=K|M>%', 'i. 0', "'4%:", '0l)x', '9+ 3', ']/$mt0', 'd2.3', '361M', '{6/\t#`B', '3.\tl3', 'g;11', '1:,"%', '\\Lcy2`;\\0$', "t1'0x", 'siAs%D}ross', '(/.W}[7', 'K=e{', 'C.2b', '.-/>', '.NhL', '/MLd', 'i.t~', 'fJS;', 'I4nnf', '~2KG1GP', 'wcJ]CQT-', 'Iekj', 'q.T^1', 'AzKfKk5!', 'kMjay', 'X1Ltv', 'UMpo', 'Lk\\;}', 'msku"Jw(1hK', '/f/l', '65Um4', 'ON6s', ' k\t7V', '|vLK', 'o;~7', '@_hD\ts', 'turn_a', 'Te)*', 'Ck\\%', 'Ptr,*', 'aK-fwuC_F', '"(YT', 'o:op_', '>eitp', 'DOUBLE', 'ZSt9t', '9foQ', 'STALLP@/+TEX', 'HANDT', '_phU-K2', '_Bloc#', 'uw16', 'WmMd', 'REYX', 'GugsR', '_OF_', ',CKh', '"pTI', 'N_MASKsc#EZ', '%n@`c', '@e{c', '!AIh(', 'rv}l1\t', '2&3I', '4l5?>NOT7', 'MPkC[G', '^Dp8u-oE', 'gYeFj', 'mEI_M', '[LvSU', 'YmVF', '[UmYT', 'gO2v', 'LOAT', 'EP1}', "CAUGH'tshp", 'ffs-3!*`\t', 'ucbl', 'UuMn', '`UQ#', '[@gj:', '%,62am', 'zHO)Cqsc,/m', '%>UCB', "@'D4H", 'R vpwl', '@GW`5', 'H|3S', '2ZWY', 'lxGXx$', '4G}Px%', 'cw]|', 'gf$z', 'RrR]R', '60WQ', 'xrQxn', 'prS|]L', 'V6grZ]Z', 'a~7Lfap', 'T.T{', 'dH7L', '030I4', 'Q+d8', 'S^ID', 'gLt5', 'V{un', 'HLj$_{h', '^dF]X', '!\\9\\.', '>$"9`', ',YYn', '07B ', ',ML 6$', 'BB$];|', "{{+' ", 'L4PC', 'x44|', "twT'Mt<4P", 'F0;*', 'UoS.sy', 'h\t?initj', 'roG$', '.ARM.', 'goUfM', 'ebug*(k', "'!@f", "6@'yp", "'lKO", "d'9#", 'rC W', "&<a'", 'h-@of', 'T@fF', '(!yL3,', 'pH\t/?', '@DO.h', 'dE!y', '4I/0Ja', 'DK.,HdL', 'O!rP', '4T^@TB', 'Hr(V\\Z', '/p@X', 'd/r1CCU', 'x 3RiF', 'iwh/M', '<H\t3', 'lCle/', 'n.d@', 'o$_-', 'Pr/Xr!r', 't 29', 'Pu_\\Y', 'uxKx', '6p/C', 'H!Eup', '\tdO6', 'O/m\t%y', '\tIo^', '.5Hl>', 'IHda', ';4CR', '(t,P', '"tOU', 'lQd0', ',VdL', 'Pot ', '34Sy', "??/'", 'z?I?', "v8\t'G6p", ' _._', '/Mz`', '/Pu.', 'q\t_x', 'q o:', 'h3QF ', 'd|?5', 'E\tw/', '/\tO8O', ' KOHO', 'R_Mv', '"_I?wa/d', '"\t_o', '\to8+#K', 'o/P#@', 'Ug to', 'Xx?$#', '<o$ ', '_UOd4', '%X?^', '2s_?', '.&,V/', '?&aOxX&$', "'a&A", "\\'K~/i')?-", '":uf', 'tstuff', 'S?BEGI', 'JCR_L', 'do_glo', 'bal\tEKKs', '_auxC', 'd.5105', ' umm', '>133', '_o)tho', 'ms4w', 'kilm', 'ma?^*', 'gdbBj', 'olvazcnc', 'mDzZ', 'S;k%', 'B|;syP', 'goTppi{pQlc', '[flm', 'gk8HTG', 't7C3', 'tHB?', 'msNq7.6', 'vfW[', 'D5@p', 'esS]{304', '8a.Wfs=Y', 'Crgs', 'n`mo8', 't1zj&', 'ssQN', '9091@', 'xpga', 'NN=48,', 'r8dv', "v'i[\t", 'skal[', 'eexf ', 'vee1', 'AmJe', '|5370a', '_\tu!', 'g:mk', 'M;64', 'WRITE', '8fa$', ',#mm&r', 'I8rf', '0tGg{', '4d*A', 'GLOBQ/8OFF', 'TABL', 'dcwX', 'V$vR', 'qT%b9', 'udprB', 'vXVZ', '$u)\t', 'cn$;)97 ', 'f{cxa', 'V([:0', '!NcZ&n', 'r@DU', 'R0bX', '[,4%', 's\tk5', 'hdgaasB', '-FbX', 'yt2a/', '\t5KG', 't(`P', '0Y>o', '6.c*-&', '`X$$h', ')Wc2', '!aE-KcC7ADD', 'j2H+', 'Xf:)', '!-hK', '1!J.', 'lc%`', 'Y !o}', '4zbC', '#Jj,', '9t8q8Fa', '\tC7i', 'X/za', '5`rl @!', 'qd*i', 'F:V+', 'kula)', '5NS$u', 'faZG', 'q!hL', 'l%Igm', 'mH7VtH\t', '_CY@', 'aPm\t\tI', 'YDhM\\{E', 'rbX\\b2', 'kN\\4IQ`', 'c=hBcV', 'fe3u', 'OtJ,/R', 'e#=-', 'T`$c1', 'I!jIN', '@H@H!(', 'UPX!', '']

```

**Command:**
```bash
mv STRINGS ../RESTRICT_EMBEDS/complete
cd ../RESTRICT_EMBEDS/
python3 RestrictToOldVersion.py
```
**Output:**
```console
Size before restriction STRINGS 200
Size after restriction STRINGS 157
```

**Command:**
```bash
mv final/STRINGS ../../XP/
cd ../../XP/
mkdir RS/
python3 RunSmallStringSet.py 
```

**Output:**
```console
# of IoT malware 157
Starting Clone Searches
100%|████████████████████| 157/157 [00:01<00:00, 88.52it/s]
StringSet 1.7849047183990479 s
```

**Command:**
```bash
cd ../Redaction/
python3 IoT_Small.py
```
**Output:**
```console
          AVG Clone Search (s) Precision Total Clone Search (s)
StringSet                0.01s     0.682                     2s
```

## PSSO on a small part of the Windows dataset (7 minutes)

**Command:**
```bash
conda activate PSS_Base
cd Windows/PSSO
unzip EMBEDS.zip
mkdir RS/
python3 RunSmallPSSO.py
```
**Output:**
```console
100%|████████████████████| 200/200 [03:53<00:00,  1.17s/it]
6 PSSO 234.02400159835815 s
```

**Command:**
```bash
cd ../Redaction/
python3 Windows_Small.py
```
**Output:**
```console
     AVG Clone Search (s) Precision Total Clone Search (s)
PSSO        1.56s (0.39s)     0.430          5h27m (5h23m)
```

## MutantX-S  on the clang v7/v4 testfield of the BinKit dataset (20 minutes)

**Command:**
```bash
conda activate PSS_Base
cd BinKiT/Normal/
unzip EMBEDS.zip
cd EMBEDS/
7z x MUTANTX2.7z
cd ../
mkdir RS/
python3 RunSmallMX.py
```
**Output:**
```console
clang-7.0/clang-4.0 7520 7520
100%|████████████████████| 7520/7520 [16:43<00:00,  7.50it/s]
clang-7.0/clang-4.0 1 MUTANTX2 1003.184271812439 s
```

**Command:**
```bash
python3 ReadSmall.py
rm -r EMBEDS/
```
**Output:**
```console
MutantX-S results only on clang-7.0_VS_clang-4.0 in one direction.
MUTANTX2 clang-7.0_VS_clang-4.0 5931 7520 0.7886968085106383 0.13317347308422656
          AVG Clone Search (s) Precision Total Clone Search (s)
MutantX-S                0.13s     0.789                 16m41s
```
