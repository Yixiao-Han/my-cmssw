import FWCore.ParameterSet.Config as cms

from RecoMuon.Configuration.RecoMuonPPonly_cff import *
from RecoHI.HiMuonAlgos.hiMuonIterativeTk_cff import *

# pretty much everything is as the pp sequence
hiReMuTracks = "hiGeneralAndRegitMuTracks" 

# global muon track
reglobalMuons = globalMuons.clone()
reglobalMuons.TrackerCollectionLabel =  hiReMuTracks

# tevMuons tracks
retevMuons    = tevMuons.clone()
retevMuons.MuonCollectionLabel = cms.InputTag("reglobalMuons")


# trackquality collections
reglbTrackQual = glbTrackQual.clone()
reglbTrackQual.InputCollection      = cms.InputTag("reglobalMuons")
reglbTrackQual.InputLinksCollection = cms.InputTag("reglobalMuons")


#recoMuons
remuons       = muons1stStep.clone()
remuons.inputCollectionLabels                   = [hiReMuTracks, 'reglobalMuons', 'standAloneMuons:UpdatedAtVtx','retevMuons:firstHit','retevMuons:picky','retevMuons:dyt']
remuons.globalTrackQualityInputTag              = cms.InputTag('reglbTrackQual')
remuons.JetExtractorPSet.JetCollectionLabel     = cms.InputTag("iterativeConePu5CaloJets")
remuons.TrackExtractorPSet.inputTrackCollection = hiReMuTracks
remuons.minPt = cms.double(0.8)

remuonEcalDetIds = muonEcalDetIds.clone()
remuonEcalDetIds.inputCollection                = "remuons"

#muons.fillGlobalTrackRefits = False

# deposits
remuIsoDepositTk = muIsoDepositTk.clone()
remuIsoDepositTk.inputTags                    = cms.VInputTag(cms.InputTag("remuons:tracker"))
remuIsoDepositJets = muIsoDepositJets.clone()
remuIsoDepositJets.inputTags                  = cms.VInputTag(cms.InputTag("remuons:jets"))
remuIsoDepositCalByAssociatorTowers = muIsoDepositCalByAssociatorTowers.clone()
remuIsoDepositCalByAssociatorTowers.inputTags = cms.VInputTag(cms.InputTag("remuons:ecal"), cms.InputTag("remuons:hcal"), cms.InputTag("remuons:ho"))

remuonShowerInformation                       = muonShowerInformation.clone()
remuonShowerInformation.muonCollection        = "remuons"

# replace the new names

remuonIdProducerTask     = cms.Task(reglbTrackQual,remuons,remuonEcalDetIds,remuonShowerInformation)
remuonIdProducerSequence = cms.Sequence(remuonIdProducerTask)

remuIsoDeposits_muonsTask= cms.Task(remuIsoDepositTk,remuIsoDepositCalByAssociatorTowers,remuIsoDepositJets)
remuIsoDeposits_muons    = cms.Sequence(remuIsoDeposits_muonsTask)

remuIsolation_muonsTask  = cms.Task(remuIsoDeposits_muonsTask)

remuIsolationTask            = cms.Task(remuIsolation_muonsTask)
remuIsolation            = cms.Sequence(remuIsolationTask)
#run this if there are no STA muons in events
muontrackingTask                    = cms.Task(standAloneMuonSeedsTask , standAloneMuons , hiRegitMuTrackingTask , reglobalMuons)
muontracking                        = cms.Sequence(muontrackingTask)

#the default setting assumes the STA is already in the event
muontracking_reTask                 = cms.Task(hiRegitMuTrackingTask , reglobalMuons)
muontracking_re                     = cms.Sequence(muontracking_reTask)
muontracking_with_TeVRefinement_reTask  = cms.Task(muontracking_reTask , retevMuons)
muontracking_with_TeVRefinement_re  = cms.Sequence(muontracking_with_TeVRefinement_reTask)
muonreco_reTask                     = cms.Task(muontracking_reTask , remuonIdProducerTask)
muonreco_re                         = cms.Sequence(muonreco_reTask)
muonrecowith_TeVRefinemen_reTask    = cms.Task(muontracking_with_TeVRefinement_reTask , remuonIdProducerTask)
muonrecowith_TeVRefinemen_re        = cms.Sequence(muonrecowith_TeVRefinemen_reTask)
muonreco_plus_isolation_reTask      = cms.Task(muonrecowith_TeVRefinemen_reTask , remuIsolationTask)
muonreco_plus_isolation_re          = cms.Sequence(muonreco_plus_isolation_reTask)

reMuonTrackRecoPbPb                 = cms.Sequence(muontracking_reTask)
# HI muon sequence (passed to RecoHI.Configuration.Reconstruction_HI_cff)
regionalMuonRecoPbPb                      = cms.Sequence(muonreco_plus_isolation_reTask)
