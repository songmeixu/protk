form Files
sentence InputDir /Users/jacobokamoto/Desktop/testdata/
sentence Ifile test
boolean PointProcessCC_RW 1
boolean PointProcessExtrema_RW 1
boolean PointProcessPeaks_RW 1
boolean PointProcessZeros_RW 1
boolean HarmonicityAC_RW 1
boolean HarmonicityCC_RW 1
boolean FormantSL_RW 1
boolean FormantBurg_RW 1
boolean LPCac_RW 1
boolean LPCBurg_RW 1
boolean LPCCovariance_RW 1
boolean LPCMarple_RW 1
boolean Silences_RW 1
boolean Intensity_RW 1
boolean MFCC_RW 1
boolean JitterLocal_RW 1
boolean JitterLocalAbsolute_RW 1
boolean JitterPPQ5_RW 1
boolean JitterRap_RW 1
boolean JitterDDP_RW 1
boolean ShimmerAPQ3_RW 1
boolean ShimmerAPQ5_RW 1
boolean ShimmerAPQ11_RW 1
boolean ShimmerLocal_RW 1
boolean ShimmerLocalDB_RW 1
boolean Pitch_RW 1
boolean PitchAC_RW 1
boolean PitchCC_RW 1
boolean PitchSHS_RW 1
boolean Sound_RW 0
endform




#### OPEN FILE ####

Read from file... 'inputDir$'/wav/'ifile$'.wav
name$ = ifile$
outputDir$ = inputDir$ - "wav/" + "praat_output/" + name$ + "_analysis/"



#global variables used later in the script
totalDuration = Get total duration

################################################### Incorporate into overall scheme
global = 1

if global
#### QUERY General Informtion ####
filedelete 'outputDir$''name $'.BasicInfo
startTime = Get start time
# fileappend 'outputDir$''name$'.BasicInfo starttime:'startTime''newline$'
endTime =Get end time
# fileappend 'outputDir$''name$'.BasicInfo endtime:'endTime''newline$'
# totalDuration = Get total duration
# fileappend 'outputDir$''name$'.BasicInfo totalduration:'totalDuration''newline$'
# numberOfChannels = Get number of channels
# fileappend 'outputDir$''name$'.BasicInfo numchannels:'numberOfChannels''newline$'
# numberOfSamples = Get number of samples
# fileappend 'outputDir$''name$'.BasicInfo numsamples:'numberOfSamples''newline$'
# samplingPeriod = Get sampling period
# fileappend 'outputDir$''name$'.BasicInfo sampleperiod'samplingPeriod''newline$'
# samplingFrequency = Get sampling frequency
# fileappend 'outputDir$''name$'.BasicInfo samplerate:'samplingFrequency''newline$'
minAmp = Get minimum... 0 0 Sinc70
fileappend 'outputDir$''name$'.BasicInfo minamp:'minAmp''newline$'
# minAmpTime = Get time of minimum... 0 0 Sinc70
# fileappend 'outputDir$''name$'.BasicInfo time_minamp:'minAmpTime''newline$'
maxAmp = Get maximum... 0 0 Sinc70
fileappend 'outputDir$''name$'.BasicInfo maxamp:'maxAmp''newline$'
# maxAmpTime = Get time of maximum... 0 0 Sinc70
# fileappend 'outputDir$''name$'.BasicInfo time_maxamp:'maxAmpTime''newline$'
absMax = Get absolute extremum... 0 0 Sinc70
fileappend 'outputDir$''name$'.BasicInfo maxabs:'absMax''newline$'
mean = Get mean... All 0 0
fileappend 'outputDir$''name$'.BasicInfo avg:'mean''newline$'
rootMeanSquare = Get root-mean-square... 0 0
fileappend 'outputDir$''name$'.BasicInfo rms:'rootMeanSquare''newline$'
standardDeviation = Get standard deviation... Average 0 0
fileappend 'outputDir$''name$'.BasicInfo stddeviation:'standardDeviation''newline$'
energy = Get energy... 0 0
fileappend 'outputDir$''name$'.BasicInfo energy:'energy''newline$'
power = Get power... 0 0
fileappend 'outputDir$''name$'.BasicInfo power:'power''newline$'
energyInAir = Get energy in air
fileappend 'outputDir$''name$'.BasicInfo energyinair:'energyInAir''newline$'
powerInAir = Get power in air
fileappend 'outputDir$''name$'.BasicInfo powerinair:'powerInAir''newline$'
intensity = Get intensity (dB)
fileappend 'outputDir$''name$'.BasicInfo intensity:'intensity''newline$'
endif



#### RAW AMPLITUDE DATA ####
if sound_RW
select Sound 'name$'
Write to short text file... 'outputDir$''name$'.Sound
endif


#### SILENCES ####
if silences_RW
select Sound 'name$'
# Minimum pitch, Time step(0=auto), silence threshhold,
#min silent interval, min sounding interval, silent interval label, sounding interval label
To TextGrid (silences)... 100 0 -25 0.1 0.1 silent sounding
Rename... 'name$'
select TextGrid 'name$'
#'name$' #########this needs to replace untitled on the previous line if Praat is an older version
Write to short text file... 'outputDir$''name$'.Silences
Remove
endif


#### PERIODICITY / PITCH ###
###todo: sub-routines on any of these. contours?

#all the pitches are written to "pitchtier" because it's infeasable to parse all of the possible in the original
if pitch_RW
select Sound 'name$'
#Time step (0=auto), Pitch Floor(Hz), Pitch Ceiling (Hz)
To Pitch... 0 75 600
Down to PitchTier
Write to short text file... 'outputDir$''name$'.Pitch
endif

if pitchAC_RW
select Sound 'name$'
#Time step (0=auto), pitch floor, max num candidates, y/n very accurate,
#silence threshold, voicing threshhold, octave cost, octave-jump cost, voiced/unvoiced cost, pitch ceiling
To Pitch (ac)... 0 75 15 no 0.03 0.45 0.01 0.35 0.14 600
Down to PitchTier
Write to short text file... 'outputDir$''name$'.PitchAC
endif

if pitchCC_RW
select Sound 'name$'
#Time step (0=auto), pitch floor, max num candidates, y/n very accurate,
#silence threshold, voicing threshhold, octave cost, octave-jump cost, voiced/unvoiced cost, pitch ceiling
To Pitch (cc)... 0 75 15 no 0.03 0.45 0.01 0.35 0.14 600
Down to PitchTier
Write to short text file... 'outputDir$''name$'.PitchCC
endif

#select Sound 'name$'
#Time step, Window length, min filter fq, max filter fq, num filters, ceiling fq, max num candidates
#To Pitch (SPINET)... 0.005 0.04 70 5000 250 500 15
#Down to PitchTier
#Write to short text file... 'outputDir$''name$'.PitchSPINET


if pitchSHS_RW
select Sound 'name$'
#time step, min pitch, max candidate num, max fq, max subharmonics,
#compression factor (<=1), ceiling hz, max points per octave
To Pitch (shs)... 0.01 50 15 1250 15 0.84 600 48
Down to PitchTier
Write to short text file... 'outputDir$''name$'.PitchSHS
endif

#### PULSES ####

#this has to be done for the jitter and shimmer to work. Can put some 'if's here later. ########RENAME HERE
select Sound 'name$'
#min pitch, max pitch (hz)
To PointProcess (periodic, cc)... 75 600
Write to short text file... 'outputDir$''name$'.PointProcessCC


### JITTER LOOP ###
jitterWindowLength = 0.125
jitterStepLength = 0.02
lastJitterMeasurement = totalDuration - 'jitterWindowLength'
iterationNumber = 'lastJitterMeasurement'/'jitterStepLength'

if jitterLocal_RW
#LOCAL#
#create file to store results.
#delete any prior existing file (have to do this since we're just appending)
filedelete 'outputDir$''name$'.JitterLocal
#write header info.
fileappend 'outputDir$''name$'.JitterLocal starttime:'startTime''newline$'
fileappend 'outputDir$''name$'.JitterLocal endtime:'endTime''newline$'
fileappend 'outputDir$''name$'.JitterLocal numdatapoints:'iterationNumber''newline$'
fileappend 'outputDir$''name$'.JitterLocal windowlength:'jitterWindowLength''newline$'
fileappend 'outputDir$''name$'.JitterLocal steplength:'jitterStepLength''newline$'
fileappend 'outputDir$''name$'.JitterLocal -----BEGIN RECORDS-----'newline$'
for i to iterationNumber - 1
start = i*'jitterStepLength'
end = i*'jitterStepLength' + 'jitterWindowLength'
jit = Get jitter (local)... start end 0.0001 0.02 1.3
fileappend 'outputDir$''name$'.JitterLocal 'start','end','jit''newline$'
endfor
endif

if jitterRap_RW
#RAP#
#create file to store results.
#delete any prior existing file (have to do this since we're just appending)
filedelete 'outputDir$''name$'.JitterRap
#write header info.
fileappend 'outputDir$''name$'.JitterRap starttime:'startTime''newline$'
fileappend 'outputDir$''name$'.JitterRap endtime:'endTime''newline$'
fileappend 'outputDir$''name$'.JitterRap numdatapoints:'iterationNumber''newline$'
fileappend 'outputDir$''name$'.JitterRap windowlength:'jitterWindowLength''newline$'
fileappend 'outputDir$''name$'.JitterRap steplength:'jitterStepLength' 'newline$'
fileappend 'outputDir$''name$'.JitterRap -----BEGIN RECORDS-----'newline$'
for i to iterationNumber - 1
start = i*'jitterStepLength'
end = i*'jitterStepLength' + 'jitterWindowLength'
jit = Get jitter (local)... start end 0.0001 0.02 1.3
fileappend 'outputDir$''name$'.JitterRap 'start','end','jit''newline$'
endfor
endif

if jitterLocalAbsolute_RW

#LocalAbsolute#
#create file to store results.
#delete any prior existing file (have to do this since we're just appending)
filedelete 'outputDir$''name$'.JitterLocalAbsolute
#write header info.
fileappend 'outputDir$''name$'.JitterLocalAbsolute starttime:'startTime''newline$'
fileappend 'outputDir$''name$'.JitterLocalAbsolute endtime:'endTime''newline$'
fileappend 'outputDir$''name$'.JitterLocalAbsolute numdatapoints:'iterationNumber''newline$'
fileappend 'outputDir$''name$'.JitterLocalAbsolute windowlength:'jitterWindowLength''newline$'
fileappend 'outputDir$''name$'.JitterLocalAbsolute steplength:'jitterStepLength' 'newline$'
fileappend 'outputDir$''name$'.JitterLocalAbsolute -----BEGIN RECORDS-----'newline$'
for i to iterationNumber - 1
start = i*'jitterStepLength'
end = i*'jitterStepLength' + 'jitterWindowLength'
jit = Get jitter (local)... start end 0.0001 0.02 1.3
fileappend 'outputDir$''name$'.JitterLocalAbsolute 'start','end','jit''newline$'
endfor
endif

if jitterPPQ5_RW
#PPQ5#
#create file to store results.
#delete any prior existing file (have to do this since we're just appending)
filedelete 'outputDir$''name$'.JitterPPQ5
#write header info.
fileappend 'outputDir$''name$'.JitterPPQ5 starttime:'startTime''newline$'
fileappend 'outputDir$''name$'.JitterPPQ5 endtime:'endTime''newline$'
fileappend 'outputDir$''name$'.JitterPPQ5 numdatapoints:'iterationNumber''newline$'
fileappend 'outputDir$''name$'.JitterPPQ5 windowlength:'jitterWindowLength''newline$'
fileappend 'outputDir$''name$'.JitterPPQ5 steplength:'jitterStepLength' 'newline$'
fileappend 'outputDir$''name$'.JitterPPQ5 -----BEGIN RECORDS-----'newline$'
for i to iterationNumber - 1
start = i*'jitterStepLength'
end = i*'jitterStepLength' + 'jitterWindowLength'
jit = Get jitter (local)... start end 0.0001 0.02 1.3
fileappend 'outputDir$''name$'.JitterPPQ5 'start','end','jit''newline$'
endfor
endif

if jitterDDP_RW
#DDP#
#create file to store results.
#delete any prior existing file (have to do this since we're just appending)
filedelete 'outputDir$''name$'.JitterDDP
#write header info.
fileappend 'outputDir$''name$'.JitterDDP starttime:'startTime''newline$'
fileappend 'outputDir$''name$'.JitterDDP endtime:'endTime''newline$'
fileappend 'outputDir$''name$'.JitterDDP numdatapoints:'iterationNumber''newline$'
fileappend 'outputDir$''name$'.JitterDDP windowlength:'jitterWindowLength''newline$'
fileappend 'outputDir$''name$'.JitterDDP steplength:'jitterStepLength' 'newline$'
fileappend 'outputDir$''name$'.JitterDDP -----BEGIN RECORDS-----'newline$'
for i to iterationNumber - 1
start = i*'jitterStepLength'
end = i*'jitterStepLength' + 'jitterWindowLength'
jit = Get jitter (local)... start end 0.0001 0.02 1.3
fileappend 'outputDir$''name$'.JitterDDP 'start','end','jit''newline$'
endfor
endif





### SHIMMER LOOP ###


#this is needed by the shimmer, so we have to do it

shimmerWindowLength = 0.125
shimmerStepLength = 0.02
lastShimmerMeasurement = totalDuration - 'shimmerWindowLength'
iterationNumber = 'lastShimmerMeasurement'/'shimmerStepLength'
select Sound 'name$'
plus PointProcess 'name$'


if shimmerLocal_RW
#Local#
#create file to store results.
#delete any prior existing file (have to do this since we're just appending)
filedelete 'outputDir$''name$'.ShimmerLocal
#write header info.
fileappend 'outputDir$''name$'.ShimmerLocal starttime:'startTime''newline$'
fileappend 'outputDir$''name$'.ShimmerLocal endtime:'endTime''newline$'
fileappend 'outputDir$''name$'.ShimmerLocal numdatapoints:'iterationNumber''newline$'
fileappend 'outputDir$''name$'.ShimmerLocal windowlength:'shimmerWindowLength''newline$'
fileappend 'outputDir$''name$'.ShimmerLocal steplength:'shimmerStepLength''newline$'
fileappend 'outputDir$''name$'.ShimmerLocal -----BEGIN RECORDS-----'newline$'
for i to iterationNumber - 1
start = i*'shimmerStepLength'
end = i*'shimmerStepLength' + 'shimmerWindowLength'
#time min, time max, shortest period, longest period, max period factor, max amplitude factor
shim = Get shimmer (local)... start end 0.0001 0.02 1.3 1.6
fileappend 'outputDir$''name$'.ShimmerLocal 'start','end','shim','newline$'
endfor
endif

if shimmerLocalDB_RW
#local_dB#
#create file to store results.
#delete any prior existing file (have to do this since we're just appending)
filedelete 'outputDir$''name$'.ShimmerLocalDB
#write header info.
fileappend 'outputDir$''name$'.ShimmerLocalDB starttime:'startTime''newline$'
fileappend 'outputDir$''name$'.ShimmerLocalDB endtime:'endTime''newline$'
fileappend 'outputDir$''name$'.ShimmerLocalDB numdatapoints:'iterationNumber''newline$'
fileappend 'outputDir$''name$'.ShimmerLocalDB windowlength:'shimmerWindowLength''newline$'
fileappend 'outputDir$''name$'.ShimmerLocalDB steplength:'shimmerStepLength''newline$'
fileappend 'outputDir$''name$'.ShimmerLocalDB -----BEGIN RECORDS-----'newline$'
for i to iterationNumber - 1
start = i*'shimmerStepLength'
end = i*'shimmerStepLength' + 'shimmerWindowLength'
#time min, time max, shortest period, longest period, max period factor, max amplitude factor
shim = Get shimmer (local_dB)... start end 0.0001 0.02 1.3 1.6
fileappend 'outputDir$''name$'.ShimmerLocalDB 'start','end','shim','newline$'
endfor
endif

if shimmerAPQ3_RW
#APQ3#
#create file to store results.
#delete any prior existing file (have to do this since we're just appending)
filedelete 'outputDir$''name$'.ShimmerAPQ3
#write header info.
fileappend 'outputDir$''name$'.ShimmerAPQ3 starttime:'startTime''newline$'
fileappend 'outputDir$''name$'.ShimmerAPQ3 endtime:'endTime''newline$'
fileappend 'outputDir$''name$'.ShimmerAPQ3 numdatapoints:'iterationNumber''newline$'
fileappend 'outputDir$''name$'.ShimmerAPQ3 windowlength:'shimmerWindowLength''newline$'
fileappend 'outputDir$''name$'.ShimmerAPQ3 steplength:'shimmerStepLength''newline$'
fileappend 'outputDir$''name$'.ShimmerAPQ3 -----BEGIN RECORDS-----'newline$'
for i to iterationNumber - 1
start = i*'shimmerStepLength'
end = i*'shimmerStepLength' + 'shimmerWindowLength'
#time min, time max, shortest period, longest period, max period factor, max amplitude factor
shim = Get shimmer (apq3)... start end 0.0001 0.02 1.3 1.6
fileappend 'outputDir$''name$'.ShimmerAPQ3 'start','end','shim','newline$'
endfor
endif

if shimmerAPQ5_RW
#APQ5#
#create file to store results.
#delete any prior existing file (have to do this since we're just appending)
filedelete 'outputDir$''name$'.ShimmerAPQ5
#write header info.
fileappend 'outputDir$''name$'.ShimmerAPQ5 starttime:'startTime''newline$'
fileappend 'outputDir$''name$'.ShimmerAPQ5 endtime:'endTime''newline$'
fileappend 'outputDir$''name$'.ShimmerAPQ5 numdatapoints:'iterationNumber''newline$'
fileappend 'outputDir$''name$'.ShimmerAPQ5 windowlength:'shimmerWindowLength''newline$'
fileappend 'outputDir$''name$'.ShimmerAPQ5 steplength:'shimmerStepLength''newline$'
fileappend 'outputDir$''name$'.ShimmerAPQ5 -----BEGIN RECORDS-----'newline$'
for i to iterationNumber - 1
start = i*'shimmerStepLength'
end = i*'shimmerStepLength' + 'shimmerWindowLength'
#time min, time max, shortest period, longest period, max period factor, max amplitude factor
shim = Get shimmer (apq5)... start end 0.0001 0.02 1.3 1.6
fileappend 'outputDir$''name$'.ShimmerAPQ5 'start','end','shim','newline$'
endfor
endif

if shimmerAPQ11_RW
#APQ11#
#create file to store results.
#delete any prior existing file (have to do this since we're just appending)
filedelete 'outputDir$''name$'.ShimmerAPQ11
#write header info.
fileappend 'outputDir$''name$'.ShimmerAPQ11 starttime:'startTime''newline$'
fileappend 'outputDir$''name$'.ShimmerAPQ11 endtime:'endTime''newline$'
fileappend 'outputDir$''name$'.ShimmerAPQ11 numdatapoints:'iterationNumber''newline$'
fileappend 'outputDir$''name$'.ShimmerAPQ11 windowlength:'shimmerWindowLength''newline$'
fileappend 'outputDir$''name$'.ShimmerAPQ11 steplength:'shimmerStepLength''newline$'
fileappend 'outputDir$''name$'.ShimmerAPQ11 -----BEGIN RECORDS-----'newline$'
for i to iterationNumber - 1
start = i*'shimmerStepLength'
end = i*'shimmerStepLength' + 'shimmerWindowLength'
#time min, time max, shortest period, longest period, max period factor, max amplitude factor
shim = Get shimmer (apq11)... start end 0.0001 0.02 1.3 1.6
fileappend 'outputDir$''name$'.ShimmerAPQ11 'start','end','shim','newline$'
endfor
endif

#leaving this out because it's not included in the config file. dunno why.
# if shimmerDDA_RW
#
# #DDA#
# #create file to store results.
# #delete any prior existing file (have to do this since we're just appending)
# filedelete 'outputDir$''name$'.ShimmerDDA
# #write header info.
# fileappend 'outputDir$''name$'.ShimmerDDA starttime:'startTime''newline$'
# fileappend 'outputDir$''name$'.ShimmerDDA endtime:'endTime''newline$'
# fileappend 'outputDir$''name$'.ShimmerDDA numdatapoints:'iterationNumber''newline$'
# fileappend 'outputDir$''name$'.ShimmerDDA windowlength:'shimmerWindowLength''newline$'
# fileappend 'outputDir$''name$'.ShimmerDDA steplength:'shimmerStepLength''newline$'
# fileappend 'outputDir$''name$'.ShimmerDDA -----BEGIN RECORDS-----'newline$'
# for i to iterationNumber - 1
# start = i*'shimmerStepLength'
# end = i*'shimmerStepLength' + 'shimmerWindowLength'
# #time min, time max, shortest period, longest period, max period factor, max amplitude factor
# shim = Get shimmer (dda)... start end 0.0001 0.02 1.3 1.6
# fileappend 'outputDir$''name$'.ShimmerDDA 'start','end','shim','newline$'
# endfor
# endif
#





if pointProcessPeaks_RW
select Sound 'name$'
#min pitch, max pitch, include maxima, include minima
To PointProcess (periodic, peaks)... 75 600 yes no
Write to short text file... 'outputDir$''name$'.PointProcessPeaks
endif

if harmonicityCC_RW
#### Harmonicity ####
select Sound 'name$'
#time step, min pitch, silence threshold, periods per window
To Harmonicity (cc)... 0.01 75 0.1 1
Write to short text file... 'outputDir$''name$'.HarmonicityCC
endif

if harmonicityAC_RW
select Sound 'name$'
#time step, min pitch, silence threshold, periods per window
To Harmonicity (ac)... 0.01 75 0.1 4.5
Write to short text file... 'outputDir$''name$'.HarmonicityAC
endif

#select Sound 'name$'
##min frequency, max frequency, bandwidth(hz), step (hz)
#To Harmonicity (gne)... 500 4500 1000 80
#Write to short text file... 'outputDir$''name$'.HarmonicityGNE




#### SPECTRUM ####

#select Sound 'name$'
#Fast/not fast
#To Spectrum... yes
#Write to short text file... 'outputDir$''name$'.Spectrum

# select Sound 'name$'
# #Bandwidth(hz)
# To Ltas... 100
# Write to short text file... 'outputDir$''name$'.Ltas

# select Sound 'name$'
# #min pitch, max pitch, max frequency, bandwidth, shortest period, longest period, max period factor
# To Ltas (pitch-corrected)... 75 600 5000 100 0.0001 0.02 1.3
# Write to short text file... 'outputDir$''name$'.LtasPitchCorrected

# #select Sound 'name$'
# #window lenth(s), max frequency, time step, freqency step, window shape
# #To Spectrogram... 0.005 5000 0.002 20 Gaussian
# #Write to short text file... 'outputDir$''name$'.Spectrogram

# #select Sound 'name$'
# #time step, freq resolution(bark), window length, forward-masking time
# #To Cochleagram... 0.01 0.1 0.03 0.03
# #Write to short text file... 'outputDir$''name$'.Cochleagram

# select Sound 'name$'
# #Window length, time step, position of filter(hz), distance btw filters(hz)
# #max frequency, relative bandwidth, min pitch(hz), max pitch(hz)
# To FormantFilter... 0.015 0.005 100 50 0 1.1 75 600
# Write to short text file... 'outputDir$''name$'.FormantFilter

select Sound 'name$'
# #window length, time step, position of first filter(bark), distance between filters(bark)
# #max frequency(bark)
# To BarkFilter... 0.015 0.005 1 1 0
# Write to short text file... 'outputDir$''name$'.BarkFilter

# select Sound 'name$'
# #Window length, time step, position of first filter(mel), dist btw filters(mel), max frequency(mel)
# To MelFilter... 0.015 0.005 100 100 0
# Write to short text file... 'outputDir$''name$'.MelFilter



#### FORMANTS ####


if formantBurg_RW
select Sound 'name$'
#time step, max number formants, max formant(hz), win length(s), pre-emphasis from (hz)
To Formant (burg)... 0 5 5500 0.025 50
Write to short text file... 'outputDir$''name$'.FormantBurg
endif

#there's a bug in the formantKeepAll short file, causing it to not parse correctly
# if formantKeepAll_RW
#
# select Sound 'name$'
# #time step, max number formants, max formant(hz), win length(s), pre-emphasis from (hz)
# To Formant (keep all)... 0 5 5500 0.025 50
# Write to short text file... 'outputDir$''name$'.FormantKeepAll
# endif

if formantSL_RW
select Sound 'name$'
#time step, max number formants, max formant(hz), win length(s), pre-emphasis from (hz)
To Formant (sl)... 0 5 5500 0.025 50
Write to short text file... 'outputDir$''name$'.FormantSL
endif


if lPCac_RW
select Sound 'name$'
#prediction order, win length, time step, pre-emphasis frequency
To LPC (autocorrelation)... 16 0.025 0.005 50
Write to short text file... 'outputDir$''name$'.LPCac
endif

if lPCCovariance_RW
select Sound 'name$'
#prediction order, win length, time step, pre-emphasis frequency
To LPC (covariance)... 16 0.025 0.005 50
Write to short text file... 'outputDir$''name$'.LPCCovariance
endif

if lPCBurg_RW
select Sound 'name$'
#prediction order, win length, time step, pre-emphasis frequency
To LPC (burg)... 16 0.025 0.005 50
Write to short text file... 'outputDir$''name$'.LPCBurg
endif

if lPCMarple_RW
select Sound 'name$'
# prediction order, win length, time step, pre-emphasis frequency, tolerance1, tolerance2
To LPC (marple)... 16 0.025 0.005 50 1e-06 1e-06
Write to short text file... 'outputDir$''name$'.LPCMarple
endif

if mFCC_RW
select Sound 'name$'
#number of coefficients, win length, time step, position of first filter(mel), dist btw filters(mel), max fq(mel)
To MFCC... 12 0.015 0.005 100 100 0
Write to short text file... 'outputDir$''name$'.MFCC
endif


# do sub-options?



#### POINTS ####

if pointProcessExtrema_RW
select Sound 'name$'
#Channel, include maxima, include minima, interpolation type
To PointProcess (extrema)... Left yes no Sinc70
Write to short text file... 'outputDir$''name$'.PointProcessExtrema
endif

if pointProcessZeros_RW
select Sound 'name$'
#channel, include raisers, include fallers
To PointProcess (zeroes)... Left yes no
Write to short text file... 'outputDir$''name$'.PointProcessZeros
endif





#### INTENSITY ####
if intensity_RW
select Sound 'name$'
#min pitch(hz), time step (0=auto), subtract mean
To Intensity... 100 0 yes
Write to short text file... 'outputDir$''name$'.Intensity
endif

select all
Remove

