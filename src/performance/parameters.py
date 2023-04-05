import numpy as np
from eventio import SimTelFile

def read_timing_pars(simtel_url, subarray):
    #not read in ctapipe
    offsets = []

    with SimTelFile(simtel_url) as f:
        for e in f:

            for tel_id in e['telescope_events'].keys():
                
                if subarray.tel[tel_id].camera.name == 'FlashCam':
                    offset = e['telescope_events'][tel_id]['header']['readout_time'] + e['telescope_events'][tel_id]['header']['relative_trigger_time']
                    offsets.append(offset)
    return offsets

def mean_true_time(source, tel_id):
    """
    Mean true time per pixel
    """
    true_time = source.file_.current_photoelectrons[tel_id-1]['time']
    trigger_pixels = source.file_.current_photoelectrons[tel_id-1]['pixel_id']

    true_mean_time = list(map(lambda x: np.mean(true_time[trigger_pixels == x]), np.unique(trigger_pixels)))
    true_std_time = list(map(lambda x: np.std(true_time[trigger_pixels == x]), np.unique(trigger_pixels)))
    
    return true_mean_time, true_std_time

def pulse_centroid(waveforms):

    centroid = np.sum(waveforms*np.repeat(np.arange(0, len(waveforms[0])), len(waveforms), axis=0), axis=-1)/np.sum(waveforms, axis=-1)
    
    return centroid

def pulse_peak(waveforms):

    return np.argmax(waveforms, axis=-1)

def noise(waveforms, start, stop):

    noise_level = np.sum(waveforms[:, start:stop], axis=-1)

    return noise_level

def noise_from_simtel(source, tel_id):

    nsb_pe_rate = source.file_.pixel_monitorings.get(tel_id, {}).get("nsb_rate")
    noise = source.file_.camera_monitorings.get(tel_id, {}).get("noise")/source.file_.camera_monitorings.get(tel_id, {}).get("n_ped_slices")
    pedestal = source.file_.camera_monitorings.get(tel_id, {}).get("pedestal")/source.file_.camera_monitorings.get(tel_id, {}).get("n_ped_slices")
    
    return nsb_pe_rate, noise, pedestal

def signal_neighbors(source, tel_id, charge):
    neighbors = source.subarray.tel[tel_id].camera.geometry.neighbor_matrix_sparse
    neighbors_indices = neighbors.indices
    neighbors_indptr = neighbors.indptr

    mean_charge_neighb = []
    for i in range(0, len(charge)):
        neighbor_arry = neighbors_indices[neighbors_indptr[i] : neighbors_indptr[i + 1]]
        mean_charge_neighb.append(np.mean(charge[neighbor_arry]))

    return mean_charge_neighb




