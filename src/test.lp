\ENCODING=ISO-8859-1
\Problem name: 

Maximize
 obj: BIOMASS_Ecoli_core_w_GAM#12
Subject To
 _13dpg_c#0:   GAPD#48 + PGK#74  = 0
 _2pg_c#1:     - _ENO#17 - PGM#76  = 0
 _3pg_c#2:     - 1.496 BIOMASS_Ecoli_core_w_GAM#12 - PGK#74 + PGM#76  = 0
 _6pgc_c#3:    - GND#56 + PGL#75  = 0
 _6pgl_c#4:    G6PDH2r#47 - PGL#75  = 0
 ac_c#5:       - ACKr#2 + ACt2r#5  = 0
 ac_e#6:       - ACt2r#5 - _EX_ac_e#19  = 0
 acald_c#7:    - ACALD#0 + ACALDt#1 + ALCD2x#9  = 0
 acald_e#8:    - ACALDt#1 - _EX_acald_e#20  = 0
 accoa_c#9:    ACALD#0 - 3.7478 BIOMASS_Ecoli_core_w_GAM#12 - CS#14 - MALS#61
               + PDH#70 + PFL#72 - PTAr#81  = 0
 acon_C_c#10:  ACONTa#3 - ACONTb#4  = 0
 actp_c#11:    ACKr#2 + PTAr#81  = 0
 adp_c#12:     ACKr#2 + 2 ADK1#6 + ATPM#10 - ATPS4r#11
               + 59.81 BIOMASS_Ecoli_core_w_GAM#12 + GLNS#50 + GLNabc#51
               + PFK#71 + PGK#74 + PPCK#79 - PYK#82 + SUCOAS#89  = 0
 akg_c#13:     - AKGDH#7 + AKGt2r#8 + 4.1182 BIOMASS_Ecoli_core_w_GAM#12
               + GLUDy#52 - GLUSy#54 + ICDHyr#58  = 0
 akg_e#14:     - AKGt2r#8 - _EX_akg_e#21  = 0
 amp_c#15:     - ADK1#6 + PPS#80  = 0
 atp_c#16:     - ACKr#2 - ADK1#6 - ATPM#10 + ATPS4r#11
               - 59.81 BIOMASS_Ecoli_core_w_GAM#12 - GLNS#50 - GLNabc#51
               - PFK#71 - PGK#74 - PPCK#79 - PPS#80 + PYK#82 - SUCOAS#89  = 0
 cit_c#17:     - ACONTa#3 + CS#14  = 0
 co2_c#18:     AKGDH#7 + CO2t#13 + GND#56 + ICDHyr#58 + ME1#64 + ME2#65
               + PDH#70 - PPC#78 + PPCK#79  = 0
 co2_e#19:     - CO2t#13 - _EX_co2_e#22  = 0
 coa_c#20:     - ACALD#0 - AKGDH#7 + 3.7478 BIOMASS_Ecoli_core_w_GAM#12 + CS#14
               + MALS#61 - PDH#70 - PFL#72 + PTAr#81 - SUCOAS#89  = 0
 dhap_c#21:    FBA#39 - TPI#94  = 0
 _e4p_c#22:    - 0.361 BIOMASS_Ecoli_core_w_GAM#12 + TALA#90 - TKT2#93  = 0
 _etoh_c#23:   - ALCD2x#9 + _ETOHt2r#18  = 0
 _etoh_e#24:   - _ETOHt2r#18 - _EX_etoh_e#23  = 0
 f6p_c#25:     - 0.0709 BIOMASS_Ecoli_core_w_GAM#12 + FBP#40 + FRUpts2#44
               - PFK#71 + PGI#73 + TALA#90 + TKT2#93  = 0
 fdp_c#26:     - FBA#39 - FBP#40 + PFK#71  = 0
 for_c#27:     FORt2#41 - FORti#42 + PFL#72  = 0
 for_e#28:     - _EX_for_e#24 - FORt2#41 + FORti#42  = 0
 fru_e#29:     - _EX_fru_e#25 - FRUpts2#44  = 0
 fum_c#30:     - FRD7#43 - FUM#45 + FUMt2_2#46 + SUCDi#88  = 0
 fum_e#31:     - _EX_fum_e#26 - FUMt2_2#46  = 0
 g3p_c#32:     - 0.129 BIOMASS_Ecoli_core_w_GAM#12 + FBA#39 - GAPD#48 - TALA#90
               + TKT1#92 + TKT2#93 + TPI#94  = 0
 g6p_c#33:     - 0.205 BIOMASS_Ecoli_core_w_GAM#12 - G6PDH2r#47 + GLCpts#49
               - PGI#73  = 0
 glc__D_e#34:  - _EX_glc__D_e#27 - GLCpts#49  = 0
 gln__L_c#35:  - 0.2557 BIOMASS_Ecoli_core_w_GAM#12 + GLNS#50 + GLNabc#51
               - GLUN#53 - GLUSy#54  = 0
 gln__L_e#36:  - _EX_gln__L_e#28 - GLNabc#51  = 0
 glu__L_c#37:  - 4.9414 BIOMASS_Ecoli_core_w_GAM#12 - GLNS#50 - GLUDy#52
               + GLUN#53 + 2 GLUSy#54 + GLUt2r#55  = 0
 glu__L_e#38:  - _EX_glu__L_e#29 - GLUt2r#55  = 0
 glx_c#39:     ICL#59 - MALS#61  = 0
 h2o_c#40:     ACONTa#3 - ACONTb#4 - ATPM#10 + ATPS4r#11
               - 59.81 BIOMASS_Ecoli_core_w_GAM#12 - CS#14 + CYTBD#15 + _ENO#17
               - FBP#40 - FUM#45 - GLNabc#51 - GLUDy#52 - GLUN#53 + H2Ot#57
               - MALS#61 - PGL#75 - PPC#78 - PPS#80  = 0
 h2o_e#41:     - _EX_h2o_e#31 - H2Ot#57  = 0
 h_c#42:       ACALD#0 + ACt2r#5 + AKGt2r#8 + ALCD2x#9 + ATPM#10 + 3 ATPS4r#11
               + 59.81 BIOMASS_Ecoli_core_w_GAM#12 + CS#14 - 2 CYTBD#15
               + D_LACt2#16 + _ETOHt2r#18 + FORt2#41 + 2 FUMt2_2#46
               + G6PDH2r#47 + GAPD#48 + GLNS#50 + GLNabc#51 + GLUDy#52
               - GLUSy#54 + GLUt2r#55 + LDH_D#60 + MALS#61 + 2 MALt2_2#62
               + MDH#63 - 4 NADH16#66 + PFK#71 + PGL#75 + PIt2r#77 + PPC#78
               + 2 PPS#80 - PYK#82 + PYRt2#83 + 2 SUCCt2_2#86 + SUCCt3#87
               + 2 THD2#91  = 0
 h_e#43:       - ACt2r#5 - AKGt2r#8 - 4 ATPS4r#11 + 2 CYTBD#15 - D_LACt2#16
               - _ETOHt2r#18 - _EX_h_e#30 - FORt2#41 - 2 FUMt2_2#46 - GLUt2r#55
               - 2 MALt2_2#62 + 3 NADH16#66 - PIt2r#77 - PYRt2#83
               - 2 SUCCt2_2#86 - SUCCt3#87 - 2 THD2#91  = 0
 icit_c#44:    ACONTb#4 - ICDHyr#58 - ICL#59  = 0
 lac__D_c#45:  D_LACt2#16 - LDH_D#60  = 0
 lac__D_e#46:  - D_LACt2#16 - _EX_lac__D_e#32  = 0
 mal__L_c#47:  FUM#45 + MALS#61 + MALt2_2#62 - MDH#63 - ME1#64 - ME2#65  = 0
 mal__L_e#48:  - _EX_mal__L_e#33 - MALt2_2#62  = 0
 nad_c#49:     - ACALD#0 - AKGDH#7 - ALCD2x#9
               - 3.547 BIOMASS_Ecoli_core_w_GAM#12 - GAPD#48 - LDH_D#60
               - MDH#63 - ME1#64 + NADH16#66 - NADTRHD#67 - PDH#70 + THD2#91
                = 0
 nadh_c#50:    ACALD#0 + AKGDH#7 + ALCD2x#9 + 3.547 BIOMASS_Ecoli_core_w_GAM#12
               + GAPD#48 + LDH_D#60 + MDH#63 + ME1#64 - NADH16#66 + NADTRHD#67
               + PDH#70 - THD2#91  = 0
 nadp_c#51:    13.0279 BIOMASS_Ecoli_core_w_GAM#12 - G6PDH2r#47 - GLUDy#52
               + GLUSy#54 - GND#56 - ICDHyr#58 - ME2#65 + NADTRHD#67 - THD2#91
                = 0
 nadph_c#52:   - 13.0279 BIOMASS_Ecoli_core_w_GAM#12 + G6PDH2r#47 + GLUDy#52
               - GLUSy#54 + GND#56 + ICDHyr#58 + ME2#65 - NADTRHD#67 + THD2#91
                = 0
 nh4_c#53:     - GLNS#50 + GLUDy#52 + GLUN#53 + NH4t#68  = 0
 nh4_e#54:     - _EX_nh4_e#34 - NH4t#68  = 0
 o2_c#55:      - 0.5 CYTBD#15 + O2t#69  = 0
 o2_e#56:      - _EX_o2_e#35 - O2t#69  = 0
 oaa_c#57:     - 1.7867 BIOMASS_Ecoli_core_w_GAM#12 - CS#14 + MDH#63 + PPC#78
               - PPCK#79  = 0
 pep_c#58:     - 0.5191 BIOMASS_Ecoli_core_w_GAM#12 + _ENO#17 - FRUpts2#44
               - GLCpts#49 - PPC#78 + PPCK#79 + PPS#80 - PYK#82  = 0
 pi_c#59:      ATPM#10 - ATPS4r#11 + 59.81 BIOMASS_Ecoli_core_w_GAM#12 + FBP#40
               - GAPD#48 + GLNS#50 + GLNabc#51 + PIt2r#77 + PPC#78 + PPS#80
               - PTAr#81 + SUCOAS#89  = 0
 pi_e#60:      - _EX_pi_e#36 - PIt2r#77  = 0
 pyr_c#61:     - 2.8328 BIOMASS_Ecoli_core_w_GAM#12 + FRUpts2#44 + GLCpts#49
               + LDH_D#60 + ME1#64 + ME2#65 - PDH#70 - PFL#72 - PPS#80 + PYK#82
               + PYRt2#83  = 0
 pyr_e#62:     - _EX_pyr_e#37 - PYRt2#83  = 0
 q8_c#63:      CYTBD#15 + FRD7#43 - NADH16#66 - SUCDi#88  = 0
 q8h2_c#64:    - CYTBD#15 - FRD7#43 + NADH16#66 + SUCDi#88  = 0
 r5p_c#65:     - 0.8977 BIOMASS_Ecoli_core_w_GAM#12 - RPI#85 - TKT1#92  = 0
 ru5p__D_c#66: GND#56 - RPE#84 + RPI#85  = 0
 s7p_c#67:     - TALA#90 + TKT1#92  = 0
 succ_c#68:    FRD7#43 + ICL#59 + SUCCt2_2#86 - SUCCt3#87 - SUCDi#88
               - SUCOAS#89  = 0
 succ_e#69:    - _EX_succ_e#38 - SUCCt2_2#86 + SUCCt3#87  = 0
 succoa_c#70:  AKGDH#7 + SUCOAS#89  = 0
 xu5p__D_c#71: RPE#84 - TKT1#92 - TKT2#93  = 0
Bounds
-1000 <= ACALD#0 <= 1000
-1000 <= ACALDt#1 <= 1000
-1000 <= ACKr#2 <= 1000
-1000 <= ACONTa#3 <= 1000
-1000 <= ACONTb#4 <= 1000
-1000 <= ACt2r#5 <= 1000
-1000 <= ADK1#6 <= 1000
 0 <= AKGDH#7 <= 1000
-1000 <= AKGt2r#8 <= 1000
-1000 <= ALCD2x#9 <= 1000
 8.39 <= ATPM#10 <= 1000
-1000 <= ATPS4r#11 <= 1000
 0 <= BIOMASS_Ecoli_core_w_GAM#12 <= 1000
-1000 <= CO2t#13 <= 1000
 0 <= CS#14 <= 1000
 0 <= CYTBD#15 <= 1000
-1000 <= D_LACt2#16 <= 1000
-1000 <= _ENO#17 <= 1000
-1000 <= _ETOHt2r#18 <= 1000
 0 <= _EX_ac_e#19 <= 1000
 0 <= _EX_acald_e#20 <= 1000
 0 <= _EX_akg_e#21 <= 1000
-1000 <= _EX_co2_e#22 <= 1000
 0 <= _EX_etoh_e#23 <= 1000
 0 <= _EX_for_e#24 <= 1000
 0 <= _EX_fru_e#25 <= 1000
 0 <= _EX_fum_e#26 <= 1000
-10 <= _EX_glc__D_e#27 <= 1000
 0 <= _EX_gln__L_e#28 <= 1000
 0 <= _EX_glu__L_e#29 <= 1000
-1000 <= _EX_h_e#30 <= 1000
-1000 <= _EX_h2o_e#31 <= 1000
 0 <= _EX_lac__D_e#32 <= 1000
 0 <= _EX_mal__L_e#33 <= 1000
-1000 <= _EX_nh4_e#34 <= 1000
-1000 <= _EX_o2_e#35 <= 1000
-1000 <= _EX_pi_e#36 <= 1000
 0 <= _EX_pyr_e#37 <= 1000
 0 <= _EX_succ_e#38 <= 1000
-1000 <= FBA#39 <= 1000
 0 <= FBP#40 <= 1000
 0 <= FORt2#41 <= 1000
 0 <= FORti#42 <= 1000
 0 <= FRD7#43 <= 1000
 0 <= FRUpts2#44 <= 1000
-1000 <= FUM#45 <= 1000
 0 <= FUMt2_2#46 <= 1000
-1000 <= G6PDH2r#47 <= 1000
-1000 <= GAPD#48 <= 1000
 0 <= GLCpts#49 <= 1000
 0 <= GLNS#50 <= 1000
 0 <= GLNabc#51 <= 1000
-1000 <= GLUDy#52 <= 1000
 0 <= GLUN#53 <= 1000
 0 <= GLUSy#54 <= 1000
-1000 <= GLUt2r#55 <= 1000
 0 <= GND#56 <= 1000
-1000 <= H2Ot#57 <= 1000
-1000 <= ICDHyr#58 <= 1000
 0 <= ICL#59 <= 1000
-1000 <= LDH_D#60 <= 1000
 0 <= MALS#61 <= 1000
 0 <= MALt2_2#62 <= 1000
-1000 <= MDH#63 <= 1000
 0 <= ME1#64 <= 1000
 0 <= ME2#65 <= 1000
 0 <= NADH16#66 <= 1000
 0 <= NADTRHD#67 <= 1000
-1000 <= NH4t#68 <= 1000
-1000 <= O2t#69 <= 1000
 0 <= PDH#70 <= 1000
 0 <= PFK#71 <= 1000
 0 <= PFL#72 <= 1000
-1000 <= PGI#73 <= 1000
-1000 <= PGK#74 <= 1000
 0 <= PGL#75 <= 1000
-1000 <= PGM#76 <= 1000
-1000 <= PIt2r#77 <= 1000
 0 <= PPC#78 <= 1000
 0 <= PPCK#79 <= 1000
 0 <= PPS#80 <= 1000
-1000 <= PTAr#81 <= 1000
 0 <= PYK#82 <= 1000
-1000 <= PYRt2#83 <= 1000
-1000 <= RPE#84 <= 1000
-1000 <= RPI#85 <= 1000
 0 <= SUCCt2_2#86 <= 1000
 0 <= SUCCt3#87 <= 1000
 0 <= SUCDi#88 <= 1000
-1000 <= SUCOAS#89 <= 1000
-1000 <= TALA#90 <= 1000
 0 <= THD2#91 <= 1000
-1000 <= TKT1#92 <= 1000
-1000 <= TKT2#93 <= 1000
-1000 <= TPI#94 <= 1000
End
