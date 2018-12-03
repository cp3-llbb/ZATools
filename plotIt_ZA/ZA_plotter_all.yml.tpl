configuration:
  include: ['centralConfig.yml']

files:
  include: {files}

plots:
  include: ['allPlots.yml']

groups:
  include: ['groups.yml']

legend:
  {legend}

systematics:
  - lumi: 1.025
  - pu
  - elidiso
  - muiso
  - muid
  #- elreco
  #- mutracking
  - jjbtaglight
  - jjbtagheavy
  - jec
  - jer 
  - trigeff
  - scaleUncorr
  - pdf
  - DY_weight11
  - DY_weight12
  - DY_weight13
  - DY_weight21
  - DY_weight22
  - DY_weight23
  - DY_weight31
  - DY_weight32
  - DY_weight33
  ##- hdamp
  ##- pdfqq
  ##- pdfgg
  ##- pdfqg
