# E13 v4 summary (random PDEs by family, 20 draws, noise [0.01], seeds [0, 1, 2, 3])

Merged rows: `benchmarks/out/e13_v4.jsonl` (from e13_v4_F1..F5). Classification: `analysis/exp/e13_summary.py` `classify` (CRASH added for rows labelled CRASH). Previous = e13_v2 (seeds 0-2) completed by e13_v3 (F5-2, seed 3).

## Pipeline, per family (v4)

| family | n | right | equivalent | abstain-ok | abstain | false-confident | other | CRASH |
|---|---|---|---|---|---|---|---|---|
| F1 | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 0 |
| F2 | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| F3 | 4 | 1 | 2 | 0 | 0 | 1 | 0 | 0 |
| F4 | 4 | 0 | 1 | 3 | 0 | 0 | 0 | 0 |
| F5 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| total | 20 | 10 | 6 | 3 | 0 | 1 | 0 | 0 |

## All methods, totals: v4 vs previous (same draws)

| method | run | n | right | equivalent | abstain-ok | abstain | false-confident | other | CRASH | right+equiv | resolvable right |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pipeline | v4 | 20 | 10 | 6 | 3 | 0 | 1 | 0 | 0 | 16 | 10/16 |
| pipeline | prev | 20 | 8 | 5 | 2 | 5 | 0 | 0 | 0 | 13 | 7/16 |
| core | v4 | 20 | 5 | 3 | 3 | 3 | 6 | 0 | 0 | 8 | 5/16 |
| core | prev | 20 | 5 | 3 | 3 | 3 | 6 | 0 | 0 | 8 | 5/16 |
| pdefind | v4 | 20 | 2 | 0 | 0 | 0 | 18 | 0 | 0 | 2 | 2/16 |
| pdefind | prev | 20 | 2 | 0 | 0 | 0 | 18 | 0 | 0 | 2 | 2/16 |
| weak_sindy | v4 | 20 | 5 | 1 | 0 | 0 | 14 | 0 | 0 | 6 | 4/16 |
| weak_sindy | prev | 20 | 5 | 1 | 0 | 0 | 14 | 0 | 0 | 6 | 4/16 |
| ensemble_sindy | v4 | 20 | 6 | 1 | 0 | 0 | 13 | 0 | 0 | 7 | 5/16 |
| ensemble_sindy | prev | 20 | 6 | 1 | 0 | 0 | 13 | 0 | 0 | 7 | 5/16 |

## Per draw, pipeline: previous -> v4

| draw | resolvable | truth | prev label | prev class | v4 label | v4 reported | v4 class | v4 time s |
|---|---|---|---|---|---|---|---|---|
| F1-0 | yes | tau - 0.0329*xi**2 - 0.513*xi | FIT-COMPATIBLE | right | FIT-COMPATIBLE | 1.0*tau - 0.0328871663691646*xi**2 - 0.513106860029777*xi | right | 61 |
| F1-1 | yes | tau - 0.42*xi | FIT-COMPATIBLE | right | FIT-COMPATIBLE | 1.0*tau - 0.420008982905183*xi | right | 15 |
| F1-2 | yes | tau + 0.0424*xi | FIT-COMPATIBLE | right | FIT-COMPATIBLE | 1.0*tau + 0.0422871520425743*xi | right | 36 |
| F1-3 | yes | tau + 0.000151*xi**4 - 0.00228*xi**3 | ID-KER | abstain | ID-KER | 1.0*tau**2 - 0.00240718427836026*tau*xi**3 - 0.00851110770907906*tau*xi**2 - 0.000207845692826645*xi**3; 1.0*tau | equivalent | 192 |
| F2-0 | yes | tau + 0.00905*I*xi**2 - 0.178*xi + 0.0764; tau - 0.00905*I*xi**2 - 0.178*xi + 0.0764 | FIT-COMPATIBLE | equivalent | FIT-COMPATIBLE | 1.0*tau + 0.00111047240955028*xi**3 - 0.194303196758754*xi + 0.0749735568307952 + 0.0067292978507107*I; 1.0*tau + 0.00111047240955028*xi**3 - 0.194303196758754*xi + 0.0749735568307952 - 0.0067292978507107*I | equivalent | 940 |
| F2-1 | yes | tau + 0.01*xi**3 - 0.0106*xi**2 - 0.0148*I*xi**2 + 0.0453*xi; tau + 0.01*xi**3 - 0.0106*xi**2 + 0.0148*I*xi**2 + 0.0453*xi | ID-KER | abstain | ID-KER | 1.0*tau + 0.00798410950951487*xi**3 - 0.0107020348381503*xi**2 + 0.0688059072515196*xi; 1.0*tau + 0.00849586896760288*xi**3 - 0.0107202038743801*xi**2 + 0.0810188981969755*xi | equivalent | 328 |
| F2-2 | yes | tau + 0.034*I*xi**2 + 0.44*xi; tau - 0.034*I*xi**2 + 0.44*xi | FIT-COMPATIBLE | right | FIT-COMPATIBLE | 1.0*tau + 0.033819587600879*I*xi**2 + 0.439348744501145*xi; 1.0*tau - 0.033819587600879*I*xi**2 + 0.439348744501145*xi | right | 458 |
| F2-3 | yes | tau + 0.00836*xi**3 - 0.00498*xi**2 + 0.368 | FIT-COMPATIBLE | right | FIT-COMPATIBLE | 1.0*tau + 0.00833065664255607*xi**3 - 0.00486225373046005*xi**2 + 0.368215701337819 | right | 52 |
| F3-0 | no | tau**2 - 0.535*tau*xi + 9.32e-5*xi**4 - 0.114*xi**2 | FIT-COMPATIBLE | right | FIT-COMPATIBLE | 1.0*tau - 0.699373621203528*xi; 1.0*tau + 0.163788595223448*xi | equivalent | 115 |
| F3-1 | yes | tau**2 - 0.11*tau*xi - 0.113*xi**2 | FIT-COMPATIBLE | equivalent | FIT-COMPATIBLE | 1.0*tau - 0.39593104021736*xi; 1.0*tau + 0.285613191724855*xi | equivalent | 94 |
| F3-2 | yes | tau**2 + 0.000974*xi**4 | UNDECIDED | abstain | UNDECIDED | 1.0*tau**2 - 6.60888216320296e-20*tau*xi**4 + 1.34476972329977e-17*tau*xi**3 + 6.78894634833409e-18*tau*xi**2 - 1.34062834155503e-16*tau*xi - 5.0383309842307e-18*tau + 0.000975081247003591*xi**4 - 3.26019593266391e-16*xi - 1.92580127374727e-15 | right | 916 |
| F3-3 | yes | tau**2 - 0.84*tau*xi + 0.0831*tau + 5.49e-5*xi**4 | FIT-COMPATIBLE | equivalent | FIT-COMPATIBLE | 1.0*tau**2 - 0.839957472995762*tau*xi + 0.0797819928206154*tau - 0.0026573221067494*xi**2 - 0.00423131426182149 | false-confident | 87 |
| F4-0 | no | tau + 2.15e-5*xi**4 - 0.000521*xi**2 + 0.0338*I*xi**2 + 0.126; tau + 2.15e-5*xi**4 - 0.000521*xi**2 - 0.0338*I*xi**2 + 0.126; tau - 0.00684*xi**2 - 0.0536*I*xi**2 + 0.0721; tau - 0.00684*xi**2 + 0.0536*I*xi**2 + 0.0721 | UNDECIDED | abstain-ok | UNDECIDED | 1.0*tau - 0.0466772575675991*xi**2; 1.0*tau + 0.136976763869929 - 0.203318999070656*I; 1.0*tau + 0.136976763869929 + 0.203318999070656*I | abstain-ok | 230 |
| F4-1 | no | tau - 0.0174*xi**2 - 0.282*xi + 0.803; tau**2 + 0.564*tau*xi + 0.834*tau + 5.04e-5*xi**4 - 0.184*xi**2 | UNDECIDED | equivalent | UNDECIDED | 1.0*tau + 0.7868449419974*xi + 0.665003889591795; 1.0*tau - 0.0152849860724455*xi**2 - 0.282257390203814*xi + 0.857779221278028; 1.0*tau - 0.220110440442798*xi + 0.203930255304078 | abstain-ok | 7114 |
| F4-2 | no | tau**2 + 0.0573*tau + 4.94e-5*xi**4 - 0.208*xi**2; tau - 0.000803*xi**2 + 0.00381*I*xi**2 + 0.332*xi; tau - 0.000803*xi**2 - 0.00381*I*xi**2 + 0.332*xi | UNDECIDED | abstain-ok | UNDECIDED | 1.0*tau + 0.309706782457033*xi + 0.0480149139429826; 1.0*tau - 0.457593257675882*xi + 0.0264967089978565; 1.0*tau + 0.453603948382196*xi | abstain-ok | 4095 |
| F4-3 | yes | tau**2 + 0.000741*xi**4 - 0.289*xi**2; tau + 0.00622*xi**4 | FIT-COMPATIBLE | equivalent | UNDECIDED | 1.0*tau - 0.0379247390264241*xi; 1.0*tau + 0.0379247390264241*xi; 1.0*tau - 0.537895999272154*xi; 1.0*tau + 0.537895999272154*xi | equivalent | 1506 |
| F5-0 | yes | tau**3 + 0.342*tau**2 - 0.427*tau*xi**2 + 0.95*tau + 0.26 | FIT-COMPATIBLE | right | FIT-COMPATIBLE | 1.0*tau**3 + 0.341380359282784*tau**2 - 0.42691007644021*tau*xi**2 + 0.952008110618065*tau + 0.258834307230156 | right | 1300 |
| F5-1 | yes | tau + 0.542; tau + 0.894*xi | FIT-COMPATIBLE | right | FIT-COMPATIBLE | 1.0*tau + 0.542088331668549; 1.0*tau + 0.894055766603114*xi | right | 54 |
| F5-2 | yes | tau**3 + 1.34*tau**2 - 0.283*tau*xi**2 + 0.996*tau + 0.271 | ID-KER | abstain | FIT-COMPATIBLE | 1.0*tau**3 + 1.33275711009909*tau**2 - 0.283533199115337*tau*xi**2 + 0.99827620685332*tau + 0.271964994413966 | right | 2214 |
| F5-3 | yes | tau**3 + 0.923*tau**2 - 0.915*tau*xi**2 + 1.8*tau + 0.519 | ID-KER | abstain | FIT-COMPATIBLE | 1.0*tau**3 + 0.920443937586889*tau**2 - 0.914315321566605*tau*xi**2 + 1.79981880359868*tau + 0.517852370158255 | right | 1346 |

## False-confident rows (v4)

- pipeline F3-3: truth ['tau**2 - 0.84*tau*xi + 0.0831*tau + 5.49e-5*xi**4'] -> FIT-COMPATIBLE ['1.0*tau**2 - 0.839957472995762*tau*xi + 0.0797819928206154*tau - 0.0026573221067494*xi**2 - 0.00423131426182149']
- core F1-3: truth ['tau + 0.000151*xi**4 - 0.00228*xi**3'] -> FIT-COMPATIBLE ['tau - 0.0022763328*xi**3']
- core F3-0: truth ['tau**2 - 0.535*tau*xi + 9.32e-5*xi**4 - 0.114*xi**2'] -> FIT-COMPATIBLE ['tau - 0.7016070998*xi + 0.0025328411', 'tau + 0.1638296533*xi - 0.0014567542']
- core F3-3: truth ['tau**2 - 0.84*tau*xi + 0.0831*tau + 5.49e-5*xi**4'] -> FIT-COMPATIBLE ['tau - 0.843189069*xi + 0.0833721028', 'tau + 0.0023582796']
- core F5-0: truth ['tau**3 + 0.342*tau**2 - 0.427*tau*xi**2 + 0.95*tau + 0.26'] -> FIT-COMPATIBLE ['tau + 0.0114272181', 'tau**2 + 0.3161891559*tau - 0.4276180478*xi**2 - 0.0015969039*xi + 0.9044569989']
- core F5-2: truth ['tau**3 + 1.34*tau**2 - 0.283*tau*xi**2 + 0.996*tau + 0.271'] -> FIT-COMPATIBLE ['tau + 0.0152436131', 'tau**2 + 0.0011653858*tau*xi**3 - 0.0032858075*tau*xi**2 + 0.0376134759*tau*xi + 1.1785413081*tau - 0.0062624346*xi**3 - 0.3028207984*xi**2 - 0.1206595217*xi + 0.4335279654']
- core F5-3: truth ['tau**3 + 0.923*tau**2 - 0.915*tau*xi**2 + 1.8*tau + 0.519'] -> FIT-COMPATIBLE ['tau + 0.04743913', 'tau**2 - 0.0045359296*tau*xi**2 + 0.0018640752*tau*xi + 0.8334013314*tau - 0.9046146106*xi**2 - 0.0053092279*xi + 1.6880480598']
- pdefind F1-0: truth ['tau - 0.0329*xi**2 - 0.513*xi'] -> n/a ['1.0*tau - 0.0146118365302*xi**2 - 0.510526263838*xi + 0.0487565440998']
- pdefind F1-3: truth ['tau + 0.000151*xi**4 - 0.00228*xi**3'] -> n/a ['1.0*tau - 0.00628528257238*xi**2 + 0.0687096343183*xi - 0.0283006469473']
- pdefind F2-0: truth ['tau + 0.00905*I*xi**2 - 0.178*xi + 0.0764', 'tau - 0.00905*I*xi**2 - 0.178*xi + 0.0764'] -> n/a ['1.0*tau - 0.191004299816*xi + 0.0764506546581']
- pdefind F2-1: truth ['tau + 0.01*xi**3 - 0.0106*xi**2 - 0.0148*I*xi**2 + 0.0453*xi', 'tau + 0.01*xi**3 - 0.0106*xi**2 + 0.0148*I*xi**2 + 0.0453*xi'] -> n/a ['1.0*tau + 0.0130752972764*xi + 0.0220231233239']
- pdefind F2-2: truth ['tau + 0.034*I*xi**2 + 0.44*xi', 'tau - 0.034*I*xi**2 + 0.44*xi'] -> n/a ['1.0*tau + 0.324378681491*xi']
- pdefind F2-3: truth ['tau + 0.00836*xi**3 - 0.00498*xi**2 + 0.368'] -> n/a ['1.0*tau - 0.0199780070333*xi + 0.375233433472']
- pdefind F3-0: truth ['tau**2 - 0.535*tau*xi + 9.32e-5*xi**4 - 0.114*xi**2'] -> n/a ['1.0*tau + 0.0115098761567*xi**2 - 0.265004151515*xi + 0.24601656439']
- pdefind F3-1: truth ['tau**2 - 0.11*tau*xi - 0.113*xi**2'] -> n/a ['1.0*tau - 0.0544217533609*xi - 0.176177257237']
- pdefind F3-2: truth ['tau**2 + 0.000974*xi**4'] -> n/a ['1.0*tau']
- pdefind F3-3: truth ['tau**2 - 0.84*tau*xi + 0.0831*tau + 5.49e-5*xi**4'] -> n/a ['1.0*tau + 0.00734658665898*xi**2 - 0.379984124621*xi + 0.202049187742']
- pdefind F4-0: truth ['tau + 2.15e-5*xi**4 - 0.000521*xi**2 + 0.0338*I*xi**2 + 0.126', 'tau + 2.15e-5*xi**4 - 0.000521*xi**2 - 0.0338*I*xi**2 + 0.126', 'tau - 0.00684*xi**2 - 0.0536*I*xi**2 + 0.0721', 'tau - 0.00684*xi**2 + 0.0536*I*xi**2 + 0.0721'] -> n/a ['1.0*tau + 0.129786227783']
- pdefind F4-1: truth ['tau - 0.0174*xi**2 - 0.282*xi + 0.803', 'tau**2 + 0.564*tau*xi + 0.834*tau + 5.04e-5*xi**4 - 0.184*xi**2'] -> n/a ['1.0*tau - 0.171312675725*xi + 0.75624417587']
- pdefind F4-2: truth ['tau**2 + 0.0573*tau + 4.94e-5*xi**4 - 0.208*xi**2', 'tau - 0.000803*xi**2 + 0.00381*I*xi**2 + 0.332*xi', 'tau - 0.000803*xi**2 - 0.00381*I*xi**2 + 0.332*xi'] -> n/a ['1.0*tau - 0.00741388523822*xi**2 + 0.0448651371275*xi - 0.103752402636']
- pdefind F4-3: truth ['tau**2 + 0.000741*xi**4 - 0.289*xi**2', 'tau + 0.00622*xi**4'] -> n/a ['1.0*tau - 0.0123161758203*xi**2 - 0.0492970388855*xi + 0.112092741191']
- pdefind F5-0: truth ['tau**3 + 0.342*tau**2 - 0.427*tau*xi**2 + 0.95*tau + 0.26'] -> n/a ['1.0*tau - 0.0310276217274*xi - 0.143756228066']
- pdefind F5-1: truth ['tau + 0.542', 'tau + 0.894*xi'] -> n/a ['1.0*tau + 0.0381957248731*xi**2 + 0.40981273362*xi + 0.64418013301']
- pdefind F5-2: truth ['tau**3 + 1.34*tau**2 - 0.283*tau*xi**2 + 0.996*tau + 0.271'] -> n/a ['1.0*tau + 0.0087987555535*xi**2 + 0.338949476495']
- pdefind F5-3: truth ['tau**3 + 0.923*tau**2 - 0.915*tau*xi**2 + 1.8*tau + 0.519'] -> n/a ['1.0*tau + 0.0784463962628*xi + 0.150170864946']
- weak_sindy F1-3: truth ['tau + 0.000151*xi**4 - 0.00228*xi**3'] -> n/a ['1.0*tau']
- weak_sindy F2-0: truth ['tau + 0.00905*I*xi**2 - 0.178*xi + 0.0764', 'tau - 0.00905*I*xi**2 - 0.178*xi + 0.0764'] -> n/a ['1.0*tau - 0.187600898622*xi + 0.0749289116369']
- weak_sindy F2-1: truth ['tau + 0.01*xi**3 - 0.0106*xi**2 - 0.0148*I*xi**2 + 0.0453*xi', 'tau + 0.01*xi**3 - 0.0106*xi**2 + 0.0148*I*xi**2 + 0.0453*xi'] -> n/a ['1.0*tau + 0.00710453454009*xi**3 - 0.0101581210597*xi**2 + 0.0621993671614*xi']
- weak_sindy F2-2: truth ['tau + 0.034*I*xi**2 + 0.44*xi', 'tau - 0.034*I*xi**2 + 0.44*xi'] -> n/a ['1.0*tau + 0.394138197192*xi']
- weak_sindy F2-3: truth ['tau + 0.00836*xi**3 - 0.00498*xi**2 + 0.368'] -> n/a ['1.0*tau + 0.00769960807663*xi**3 + 0.369950960454']
- weak_sindy F3-2: truth ['tau**2 + 0.000974*xi**4'] -> n/a ['1.0*tau', '1.0*tau']
- weak_sindy F3-3: truth ['tau**2 - 0.84*tau*xi + 0.0831*tau + 5.49e-5*xi**4'] -> n/a ['1.0*tau', '1.0*tau - 0.834869950987*xi']
- weak_sindy F4-0: truth ['tau + 2.15e-5*xi**4 - 0.000521*xi**2 + 0.0338*I*xi**2 + 0.126', 'tau + 2.15e-5*xi**4 - 0.000521*xi**2 - 0.0338*I*xi**2 + 0.126', 'tau - 0.00684*xi**2 - 0.0536*I*xi**2 + 0.0721', 'tau - 0.00684*xi**2 + 0.0536*I*xi**2 + 0.0721'] -> n/a ['1.0*tau + 0.00580692465125*xi**3 - 0.0524277219372*xi**2 + 0.0505277534114']
- weak_sindy F4-1: truth ['tau - 0.0174*xi**2 - 0.282*xi + 0.803', 'tau**2 + 0.564*tau*xi + 0.834*tau + 5.04e-5*xi**4 - 0.184*xi**2'] -> n/a ['1.0*tau**2 - 0.02192377494*tau*xi**3 - 0.0810926621998*tau*xi**2 + 0.224153476233*tau*xi + 1.30284952823*tau - 0.0304291393074*xi**3 - 0.203326254427*xi**2 + 0.45857933287']
- weak_sindy F4-2: truth ['tau**2 + 0.0573*tau + 4.94e-5*xi**4 - 0.208*xi**2', 'tau - 0.000803*xi**2 + 0.00381*I*xi**2 + 0.332*xi', 'tau - 0.000803*xi**2 - 0.00381*I*xi**2 + 0.332*xi'] -> n/a ['1.0*tau**2 + 0.0659518871862*tau*xi**2 + 0.311327804841*tau - 0.0105797733283*xi**3 - 0.25140349704*xi**2 - 0.187756803403']
- weak_sindy F4-3: truth ['tau**2 + 0.000741*xi**4 - 0.289*xi**2', 'tau + 0.00622*xi**4'] -> n/a ['1.0*tau**2 + 0.0117294717486*tau*xi**3 - 0.035692476109*tau*xi**2 + 0.0962537527148*tau*xi + 0.0987796822203*tau + 0.00577558738246*xi**4 - 0.0137423022505*xi**3 - 0.161917730796*xi**2 - 0.0659788016015*xi + 0.200713668525']
- weak_sindy F5-0: truth ['tau**3 + 0.342*tau**2 - 0.427*tau*xi**2 + 0.95*tau + 0.26'] -> n/a ['1.0*tau + 0.170554922867*xi']
- weak_sindy F5-2: truth ['tau**3 + 1.34*tau**2 - 0.283*tau*xi**2 + 0.996*tau + 0.271'] -> n/a ['1.0*tau + 0.111243686299*xi**2 + 0.679498699677']
- weak_sindy F5-3: truth ['tau**3 + 0.923*tau**2 - 0.915*tau*xi**2 + 1.8*tau + 0.519'] -> n/a ['1.0*tau + 0.0205286298815*xi**4']
- ensemble_sindy F1-3: truth ['tau + 0.000151*xi**4 - 0.00228*xi**3'] -> n/a ['1.0*tau']
- ensemble_sindy F2-0: truth ['tau + 0.00905*I*xi**2 - 0.178*xi + 0.0764', 'tau - 0.00905*I*xi**2 - 0.178*xi + 0.0764'] -> n/a ['1.0*tau - 0.187559944744*xi + 0.0748049169142']
- ensemble_sindy F2-1: truth ['tau + 0.01*xi**3 - 0.0106*xi**2 - 0.0148*I*xi**2 + 0.0453*xi', 'tau + 0.01*xi**3 - 0.0106*xi**2 + 0.0148*I*xi**2 + 0.0453*xi'] -> n/a ['1.0*tau + 0.00711747327967*xi**3 - 0.0102116110701*xi**2 + 0.0622420205255*xi']
- ensemble_sindy F2-2: truth ['tau + 0.034*I*xi**2 + 0.44*xi', 'tau - 0.034*I*xi**2 + 0.44*xi'] -> n/a ['1.0*tau + 0.393592978876*xi']
- ensemble_sindy F3-2: truth ['tau**2 + 0.000974*xi**4'] -> n/a ['1.0*tau', '1.0*tau']
- ensemble_sindy F3-3: truth ['tau**2 - 0.84*tau*xi + 0.0831*tau + 5.49e-5*xi**4'] -> n/a ['1.0*tau', '1.0*tau - 0.830140662797*xi']
- ensemble_sindy F4-0: truth ['tau + 2.15e-5*xi**4 - 0.000521*xi**2 + 0.0338*I*xi**2 + 0.126', 'tau + 2.15e-5*xi**4 - 0.000521*xi**2 - 0.0338*I*xi**2 + 0.126', 'tau - 0.00684*xi**2 - 0.0536*I*xi**2 + 0.0721', 'tau - 0.00684*xi**2 + 0.0536*I*xi**2 + 0.0721'] -> n/a ['1.0*tau + 0.00567728245763*xi**3 - 0.0525269282076*xi**2 + 0.0502652282407']
- ensemble_sindy F4-1: truth ['tau - 0.0174*xi**2 - 0.282*xi + 0.803', 'tau**2 + 0.564*tau*xi + 0.834*tau + 5.04e-5*xi**4 - 0.184*xi**2'] -> n/a ['1.0*tau**2 - 0.0206489973924*tau*xi**3 - 0.0695813146625*tau*xi**2 + 0.242564732855*tau*xi + 1.3752387858*tau - 0.0309635969038*xi**3 - 0.192234270471*xi**2 + 0.520488904636']
- ensemble_sindy F4-2: truth ['tau**2 + 0.0573*tau + 4.94e-5*xi**4 - 0.208*xi**2', 'tau - 0.000803*xi**2 + 0.00381*I*xi**2 + 0.332*xi', 'tau - 0.000803*xi**2 - 0.00381*I*xi**2 + 0.332*xi'] -> n/a ['1.0*tau**2 + 0.0621157447787*tau*xi**2 + 0.303440869535*tau - 0.0120878851146*xi**3 - 0.252558993361*xi**2 - 0.201126514844']
- ensemble_sindy F4-3: truth ['tau**2 + 0.000741*xi**4 - 0.289*xi**2', 'tau + 0.00622*xi**4'] -> n/a ['1.0*tau**2 + 0.0112667130844*tau*xi**3 - 0.0394751550562*tau*xi**2 + 0.0952305474632*tau*xi + 0.103839691309*tau + 0.00722635048081*xi**4 - 0.0139876264177*xi**3 - 0.148207057264*xi**2 - 0.0653803566524*xi + 0.204297567154']
- ensemble_sindy F5-0: truth ['tau**3 + 0.342*tau**2 - 0.427*tau*xi**2 + 0.95*tau + 0.26'] -> n/a ['1.0*tau + 0.167422064157*xi']
- ensemble_sindy F5-2: truth ['tau**3 + 1.34*tau**2 - 0.283*tau*xi**2 + 0.996*tau + 0.271'] -> n/a ['1.0*tau + 0.116827169788*xi**2 - 0.0310069049925*xi + 0.688462710355']
- ensemble_sindy F5-3: truth ['tau**3 + 0.923*tau**2 - 0.915*tau*xi**2 + 1.8*tau + 0.519'] -> n/a ['1.0*tau + 0.0245901871381*xi**4 + 0.0188721143981*xi**3 + 0.181694243702*xi + 0.246853208328']

## CRASH / other rows (v4)

- none

## Note

- Pipeline v4 vs previous (v2+v3, same 20 draws, 1 % noise): right 8 -> 10, right+equivalent 13 -> 16,
  wrong abstentions on resolvable draws 5 -> 0, false-confident 0 -> 1, no CRASH.
  Resolvable draws answered exactly: 7/16 -> 10/16.
- Gains: F5-2, F5-3 (ID-KER -> right), F3-2 (UNDECIDED, but the reported law matches: `ok` True),
  F1-3 and F2-1 (ID-KER abstain -> equivalent; still labelled ID-KER).
- Regression: F3-3 equivalent -> false-confident. The tau^2, tau*xi, tau terms are right, but v4 reports
  -0.00266 xi^2 - 0.00423 in place of the truth's 5.49e-5 xi^4, which fails the dchi2 <= 25 equivalence test.
  Also F3-0 (not resolvable) right -> equivalent, F4-3 FIT-COMPATIBLE equivalent -> UNDECIDED equivalent.
- core and the SINDy methods give the same classes as before (deterministic on the same inputs). SINDy has
  no abstention: pdefind 18, weak_sindy 14, ensemble_sindy 13 of 20 wrong answers (false-confident by the
  E13 scoring rule).
- Cost: F4 is slow, pipeline 230 / 7114 / 4095 / 1506 s per draw (F4-1 about 2 h); F5 1300-2214 s.
