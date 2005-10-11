#ifndef EBLaserTask_H
#define EBLaserTask_H

/*
 * \file EBLaserTask.h
 *
 * $Date: 2005/10/08 08:55:06 $
 * $Revision: 1.4 $
 * \author G. Della Ricca
 *
*/

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include <FWCore/Framework/interface/EDAnalyzer.h>

#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/MakerMacros.h>

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DQMServices/Core/interface/DaqMonitorBEInterface.h"
#include "DQMServices/Daemon/interface/MonitorDaemon.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include <DataFormats/EcalDigi/interface/EcalDigiCollections.h>
#include <DataFormats/EcalDetId/interface/EBDetId.h>
#include <DataFormats/EcalDigi/interface/EBDataFrame.h>

#include <DQM/EcalBarrelMonitorTasks/interface/EBMonitorUtils.h>

#include <iostream>
#include <fstream>
#include <vector>

using namespace cms;
using namespace std;

class EBLaserTask: public edm::EDAnalyzer{

friend class EcalBarrelMonitorModule;

public:

/// Constructor
EBLaserTask(const edm::ParameterSet& ps, DaqMonitorBEInterface* dbe);

/// Destructor
virtual ~EBLaserTask();

protected:

/// Analyze digis out of raw data
void analyze(const edm::Event& e, const edm::EventSetup& c);

private:

int ievt;

MonitorElement* meShapeMapL1[36];
MonitorElement* meAmplMapL1[36];

MonitorElement* meShapeMapL2[36];
MonitorElement* meAmplMapL2[36];

ofstream logFile;

};

#endif
