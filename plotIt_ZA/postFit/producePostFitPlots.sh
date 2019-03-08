#!/usr/bin/env bash

get_legend() {

    local legend=""
    case $1 in
        800_400)
            legend="rho steps for 800,400" ;;

    esac

    echo $legend
}

get_legend_2d() {
    legend=$(get_legend $1)
    echo "${legend}, m_{jj} bins"
}

#signals="MH-800_MA-200 MH-1000_MA-200 MH-800_MA-50 MH-500_MA-400 MH-800_MA-100 MH-650_MA-50 MH-250_MA-50 MH-1000_MA-50 MH-500_MA-50 MH-800_MA-400 MH-500_MA-300 MH-300_MA-100 MH-500_MA-200 MH-250_MA-100 MH-1000_MA-500 MH-300_MA-50 MH-800_MA-700 MH-200_MA-100 MH-200_MA-50 MH-300_MA-200 MH-500_MA-100"
#signals="300p00_200p00 300p00_100p00 200p00_100p00"
signals="261p40_150p50 609p21_505p93"
#signals="1000p00_200p00
#1000p00_500p00
#1000p00_50p00
#132p00_30p00
#132p00_37p34
#143p44_30p00
#143p44_37p34
#143p44_46p48
#157p77_30p00
#157p77_37p34
#157p77_46p48
#157p77_57p85
#173p52_30p00
#173p52_37p34
#173p52_46p48
#173p52_57p85
#173p52_72p01
#190p85_30p00
#190p85_37p34
#190p85_46p48
#190p85_57p85
#190p85_71p28
#190p85_86p78
#200p00_100p00
#200p00_50p00
#209p90_104p53
#209p90_30p00
#209p90_37p34
#209p90_46p48
#209p90_57p71
#209p90_71p15
#209p90_86p79
#230p77_102p72
#230p77_123p89
#230p77_30p00
#230p77_37p10
#230p77_45p88
#230p77_56p73
#230p77_69p78
#230p77_85p09
#250p00_100p00
#250p00_50p00
#261p40_102p99
#261p40_124p53
#261p40_150p50
#261p40_37p10
#261p40_45p88
#261p40_56p73
#261p40_69p66
#261p40_85p10
#296p10_120p82
#296p10_145p93
#296p10_176p02
#296p10_30p00
#296p10_36p79
#296p10_45p12
#296p10_55p33
#296p10_67p65
#296p10_82p40
#296p10_99p90
#300p00_100p00
#300p00_200p00
#300p00_50p00
#335p40_120p39
#335p40_145p06
#335p40_174p55
#335p40_209p73
#335p40_30p00
#335p40_36p79
#335p40_45p12
#335p40_55p33
#335p40_67p54
#335p40_82p14
#335p40_99p61
#379p00_118p81
#379p00_143p08
#379p00_171p71
#379p00_205p76
#379p00_246p30
#379p00_30p00
#379p00_36p63
#379p00_44p72
#379p00_54p59
#379p00_66p57
#379p00_80p99
#379p00_98p26
#442p63_113p53
#442p63_135p44
#442p63_161p81
#442p63_193p26
#442p63_230p49
#442p63_274p57
#442p63_30p00
#442p63_327p94
#442p63_36p64
#442p63_44p76
#442p63_54p67
#442p63_66p49
#442p63_80p03
#442p63_95p27
#500p00_100p00
#500p00_200p00
#500p00_300p00
#500p00_400p00
#500p00_50p00
#516p94_109p30
#516p94_128p58
#516p94_151p69
#516p94_179p35
#516p94_212p14
#516p94_250p63
#516p94_296p65
#516p94_30p00
#516p94_352p61
#516p94_36p47
#516p94_423p96
#516p94_44p34
#516p94_53p90
#516p94_65p52
#516p94_78p52
#516p94_93p12
#609p21_116p29
#609p21_135p66
#609p21_158p41
#609p21_185p18
#609p21_216p52
#609p21_253p68
#609p21_298p01
#609p21_30p00
#609p21_34p86
#609p21_351p22
#609p21_40p51
#609p21_417p76
#609p21_47p08
#609p21_505p93
#609p21_54p71
#609p21_63p58
#609p21_85p86
#609p21_99p78
#650p00_50p00
#717p96_116p19
#717p96_157p56
#717p96_183p48
#717p96_213p73
#717p96_249p34
#717p96_291p34
#717p96_30p00
#717p96_341p02
#717p96_34p86
#717p96_400p03
#717p96_40p51
#717p96_475p80
#717p96_47p08
#717p96_54p71
#717p96_577p65
#717p96_63p58
#717p96_73p89
#717p96_85p86
#717p96_99p78
#800p00_100p00
#800p00_200p00
#800p00_400p00
#800p00_50p00
#800p00_700p00
#846p11_101p43
#846p11_118p11
#846p11_137p54
#846p11_160p17
#846p11_186p51
#846p11_217p19
#846p11_252p91
#846p11_294p51
#846p11_30p00
#846p11_345p53
#846p11_34p93
#846p11_405p40
#846p11_40p68
#846p11_475p64
#846p11_47p37
#846p11_558p06
#846p11_55p16
#846p11_64p24
#846p11_654p75
#846p11_74p80
#846p11_87p10
#997p14_101p43
#997p14_118p11
#997p14_137p54
#997p14_160p17
#997p14_186p51
#997p14_217p19
#997p14_254p82
#997p14_298p97
#997p14_30p00
#997p14_34p93
#997p14_350p77
#997p14_40p68
#997p14_411p54
#997p14_47p37
#997p14_482p85
#997p14_55p16
#997p14_566p51
#997p14_64p24
#997p14_664p66
#997p14_74p80
#997p14_779p83
#997p14_87p10"

flavors="MuMu ElEl MuEl"

for flavor in $flavors; do
  for signal in $signals; do

    root="postFitShapes/${signal}/$flavor"
    output="postFitPlots/$signal/$flavor"

    input="${root}"

    echo $input

    legend=$(get_legend $signal)
    legend_2d=$(get_legend_2d $signal)

    sed "s|#ROOT#|${input}|g" centralConfig_shapes_postfit.yml.tpl > centralConfig_shapes_postfit.yml

    # Uncomment signal point
    cp MCFiles_shapes_postfit.yml.tpl MCFiles_shapes_postfit.yml
    #sed -i "/,+7 s/#//" MCFiles_shapes_postfit.yml

    # Replace signal and legend
    sed "s/#SIGNAL#/${signal}/g" postfitPlots.yml.tpl > postfitPlots.yml
    #sed -i "s/#LEGEND_NN#/\"${legend}\"/g" postfitPlots.yml
    #sed -i "s/#LEGEND_2D#/\"${legend_2d}\"/g" postfitPlots.yml
    if [ $flavor = "MuMu" ]; then
      sed -i "s/#CHANNEL#/#mu#mu channel/" postfitPlots.yml
    elif [ $flavor = "ElEl" ]; then
      sed -i "s/#CHANNEL#/ee channel/" postfitPlots.yml
    else
      sed -i "s/#CHANNEL#/#mue + e#mu channel/" postfitPlots.yml
    fi

    cp postfitPlots.yml postfitPlots_${signal}_${flavor}.yml

    ../../../plotIt/plotIt -o ${output} -- ZA_plotter_all_shapes_postfit.yml

    #rm postfitPlots.yml
    #rm MCFiles_shapes_postfit.yml
    #rm centralConfig_shapes_postfit.yml
  done
done
