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
  - elreco
  - elidiso
  - mutracking
  - muiso
  - muid
  - jjbtaglight
  - jjbtagheavy
  - jec
  - jer 
  - trigeff
  - scaleUncorr
  - pdf
  - hdamp
  #- pdfqq
  #- pdfgg
  #- pdfqg
