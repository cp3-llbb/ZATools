#FIXME: Add other minor backgrounds one run in Combine

# HIGGS

'SMHiggs_postfit_histos.root':
  type: mc
  group: Other

# VV

'VV_postfit_histos.root':
  type: mc
  group: VV(V)

# VVV

'VV_postfit_histos.root':
  type: mc
  group: VV(V)

# Single top

'SingleTop_postfit_histos.root':
  type: mc
  group: t

# TT

'ttbar_postfit_histos.root':
  type: mc
  group: tt

# DY

'dy_mc_postfit_histos.root':
  type: mc
  group: DY

# Add Signal

#'HToZATo2L2B_500p00_200p00_v6.1.0+80X_ZAAnalysis_2018-02-16-4-g786cd83_histos.root':
#  type: signal
#  #Scale by sigma*BR*35922*1000 (because signal xsec=1fb in samadhi)
#  #Like this is will be normalized to sigma*BR in pb
#  scale: 7184400 #normalize to 0.2pb
#  line-color: '#9467bd' #purple
#  legend: 'Signal'
#  legend-order: 14 
#  size: 40
#  line-width: 2.7
#  line-type: 1

'HToZATo2L2B_442p63_193p26_v6.1.0+80X_ZAAnalysis_2018-02-16-4-g786cd83_histos.root':
  type: signal
  #scale by theor. x-sec*BR (=0.163) * 35922 * 1000 (because signal xsec=1fb in samadhi)
  #scale: 5873970
  scale: 35922000
  #line-color: '#9467bd' #purple
  line-color: '#393b79' #dark blue
  #line-color: '#636363' #gray
  legend: 'M_{H},M_{A} = 442,193 GeV'
  #legend: 'Signal'
  legend-order: 14 
  size: 10
  line-width: 3
  line-type: 1

#'HToZATo2L2B_261p40_150p50_v6.1.0+80X_ZAAnalysis_2018-02-16-4-g786cd83_histos.root':
#  type: signal
#  #scale by theor. x-sec*BR (=0.59) * 35922 * 1000 (because signal xsec=1fb in samadhi)
#  #scale: 21193980
#  #scale: 33795417.6 #used for figure in paper
#  #scale: 21296144 
#  #scale: 12230879.48
#  scale: 35922000
#  #line-color: '#9467bd' #purple
#  line-color: '#393b79' #dark blue
#  #line-color: '#636363' #gray
#  legend: 'M_{H},M_{A} = 261,150 GeV'
#  #legend: 'Signal'
#  legend-order: 14 
#  size: 40
#  line-width: 3
#  line-type: 1

#'HToZATo2L2B_609p21_505p93_v6.1.0+80X_ZAAnalysis_2018-02-16-4-g786cd83_histos.root':
#  type: signal
#  #scale by theor. x-sec * 35922 * 1000 (because signal xsec=1fb in samadhi)
#  scale: 98.26
#  line-color: '#9467bd' #purple
#  legend: '2HDM (609,505)'
#  legend-order: 14 
#  size: 40
#  line-width: 3
#  line-type: 1



#CHANGE THE CROSS SECTION UNTIL IT FITS THE EXCESS
#'HToZATo2L2B_500p00_200p00_v6.1.0+80X_ZAAnalysis_2018-02-16-4-g786cd83_histos.root':
#  type: signal
#  #Scale by sigma*BR*35922*1000 (because signal xsec=1fb in samadhi)
#  #Like this is will be normalized to sigma*BR in pb
#  scale: 3184400 #normalize to 0.2pb
#  line-color: '#9467bd' #purple
#  legend: 'Signal'
#  legend-order: 14 
#  size: 40
#  line-width: 2.7
#  line-type: 1



