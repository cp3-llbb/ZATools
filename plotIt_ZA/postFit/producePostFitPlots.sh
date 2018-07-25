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

signals="MH-800_MA-200 MH-1000_MA-200 MH-800_MA-50 MH-500_MA-400 MH-800_MA-100 MH-650_MA-50 MH-250_MA-50 MH-1000_MA-50 MH-500_MA-50 MH-800_MA-400 MH-500_MA-300 MH-300_MA-100 MH-500_MA-200 MH-250_MA-100 MH-1000_MA-500 MH-300_MA-50 MH-800_MA-700 MH-200_MA-100 MH-200_MA-50 MH-300_MA-200 MH-500_MA-100"

flavors="MuMu ElEl"

for flavor in $flavors; do
  for signal in $signals; do

    root="postFitShapes/${signal}_noMuEl/$flavor"
    output="postFitPlots/$signal/$flavor"
    
    input="${root}"

    legend=$(get_legend $signal)
    legend_2d=$(get_legend_2d $signal)

    sed "s|#ROOT#|${input}|g" centralConfig_shapes_postfit.yml.tpl > centralConfig_shapes_postfit.yml

    # Uncomment signal point
    cp MCFiles_shapes_postfit.yml.tpl MCFiles_shapes_postfit.yml
    sed -i "/,+7 s/#//" MCFiles_shapes_postfit.yml

    # Replace signal and legend
    sed "s/#SIGNAL#/${signal}/g" postfitPlots.yml.tpl > postfitPlots.yml
    #sed -i "s/#LEGEND_NN#/\"${legend}\"/g" postfitPlots.yml
    #sed -i "s/#LEGEND_2D#/\"${legend_2d}\"/g" postfitPlots.yml
    if [ $flavor = "MuMu" ]; then
      sed -i "s/#CHANNEL#/#mu#mu channel/" postfitPlots.yml
    else
      sed -i "s/#CHANNEL#/ee channel/" postfitPlots.yml
    fi

    cp postfitPlots.yml postfitPlots_${signal}_${flavor}.yml

    ../../../plotIt/plotIt -o ${output} -- hh_plotter_all_shapes_postfit.yml

    #rm postfitPlots.yml

    rm postfitPlots.yml
    rm MCFiles_shapes_postfit.yml
    rm centralConfig_shapes_postfit.yml
  done
done

# Do ptjj & mjj for 400 GeV
#for signal in $signals; do

#    input="${root}"

#    sed "s|#ROOT#|${input}|g" centralConfig_shapes_postfit.yml.tpl > centralConfig_shapes_postfit.yml

#    cp MCFiles_shapes_postfit.yml.tpl MCFiles_shapes_postfit.yml

#    # Uncomment signal points
#    for other_signal in $signals; do
#        sed -i "/${other_signal}/,+7 s/#//" MCFiles_shapes_postfit.yml
#    done
#
#    # MuMu

#    # Uncomment pt jj plots
#    sed "/ptjj_/,+13 s/#//" postfitPlots.yml.tpl > postfitPlots.yml
#    sed -i "/mjj_/,+13 s/#//" postfitPlots.yml

#    # Comment all the rest NN plots
#    sed -i "/#SIGNAL#/,$ s/^/#/" postfitPlots.yml

#    sed -i "s/#CHANNEL#/#mu#mu channel/" postfitPlots.yml

#    cat postfitPlots.yml

#    ../../../plotIt/plotIt -o ${output} -- hh_plotter_all_shapes_postfit.yml

#    # Restore
#    rm postfitPlots.yml
#    rm MCFiles_shapes_postfit.yml
#    rm centralConfig_shapes_postfit.yml
#done
