rho_steps:
  labels:
  - position: [0.22, 0.895]
    size: 35
    text: '#CHANNEL#'
  legend-columns: 2
  save-extensions: [pdf, png]
  show-errors: true
  show-overflow: false
  show-ratio: true
  log-y: both
  # For 442, 193
  y-axis-range: [0,6300]  #MuMu+ElEl
  #y-axis-range: [0,2050]  #MuEl
  # For 261_150
  #y-axis-range: [0,1700]  #ElEl
  #y-axis-range: [0,3800]  #MuMu
  #y-axis-range: [0,5200]  #MuMu+ElEl
  #y-axis-range: [0,1500]  #MuEl
  # For 609, 505
  #y-axis-range: [0,1700]  #ElEl
  #y-axis-range: [0,3000]  #MuMu
  # For 627, 162
  #y-axis-range: [0,1600]  #ElEl
  #y-axis-range: [0,3700]  #MuMu
  # For 371, 57 
  #y-axis-range: [0,750]  #ElEl
  #y-axis-range: [0,1900]  #MuMu
  
  x-axis: '#rho'
  y-axis: Events
  y-axis-format: '%1% / %2$.2f GeV'
