import FWCore.ParameterSet.Config as cms


# creates the recoGsfTracks_electronGsfTracks__RECO = input GSF tracks
from TrackingTools.GsfTracking.GsfElectronTracking_cff import *
ecalDrivenElectronSeeds.SeedConfiguration.initialSeeds = "hiPixelTrackSeeds"
electronCkfTrackCandidates.src = "ecalDrivenElectronSeeds"

ecalDrivenElectronSeeds.SeedConfiguration.maxHOverEBarrel = cms.double(0.25)
ecalDrivenElectronSeeds.SeedConfiguration.maxHOverEEndcaps = cms.double(0.25)

electronGsfTrackingHiTask = cms.Task(ecalDrivenElectronSeeds ,
                                     electronCkfTrackCandidates ,
                                     electronGsfTracks)
electronGsfTrackingHi = cms.Sequence(electronGsfTrackingHiTask)

# run the supercluster(EE+EB)-GSF track association ==> output: recoGsfElectrons_gsfElectrons__RECO
from RecoEgamma.EgammaElectronProducers.gsfElectronSequence_cff import *
from RecoParticleFlow.PFProducer.pfElectronTranslator_cff import *
gsfElectrons.ctfTracks     = cms.InputTag("hiGeneralTracks")
gsfElectronCores.ctfTracks = cms.InputTag("hiGeneralTracks")
pfElectronTranslator.emptyIsOk = cms.bool(True)

gsfElectrons.fillConvVtxFitProb = cms.bool(False)

ecalDrivenGsfElectrons.ctfTracksTag = cms.InputTag("hiGeneralTracks")
ecalDrivenGsfElectronCores.ctfTracks = cms.InputTag("hiGeneralTracks")
ecalDrivenGsfElectrons.vtxTag = cms.InputTag("hiSelectedVertex")

ecalDrivenGsfElectrons.preselection.maxHOverEBarrelCone = cms.double(0.25)
ecalDrivenGsfElectrons.preselection.maxHOverEEndcapsCone = cms.double(0.25)
ecalDrivenGsfElectrons.preselection.maxHOverEBarrelTower = cms.double(0.)
ecalDrivenGsfElectrons.preselection.maxHOverEEndcapsTower = cms.double(0.)
ecalDrivenGsfElectrons.fillConvVtxFitProb = cms.bool(False)


from RecoParticleFlow.PFTracking.pfTrack_cfi import *
pfTrack.UseQuality = cms.bool(True)
pfTrack.TrackQuality = cms.string('highPurity')
pfTrack.TkColList = cms.VInputTag("hiGeneralTracks")
pfTrack.PrimaryVertexLabel = cms.InputTag("hiSelectedVertex")
pfTrack.MuColl = cms.InputTag("hiMuons1stStep")

from RecoParticleFlow.PFTracking.pfTrackElec_cfi import *
pfTrackElec.applyGsfTrackCleaning = cms.bool(True)
pfTrackElec.PrimaryVertexLabel = cms.InputTag("hiSelectedVertex")

hiElectronTask = cms.Task(electronGsfTrackingHiTask ,   
                                  pfTrack ,
                                  pfTrackElec ,
                                  gsfEcalDrivenElectronTask 
                                  )
hiElectronSequence = cms.Sequence(hiElectronTask)
