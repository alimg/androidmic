package com.alimgokkaya.androidmic;

import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import android.util.Log;

/**
 * Created by alim on 1/20/14.
 */
public class RecordThread extends Thread{

    private final int sampleRate;
    private final int bufferSize;
    private final RecordingListener listener;
    private boolean running=true;

    public RecordThread(int sampleRate, int bufferSize, RecordingListener listener){
        this.sampleRate=sampleRate;
        this.bufferSize=bufferSize;
        this.listener = listener;
    }

    @Override
    public void run() {
        AudioRecord audio = new AudioRecord(MediaRecorder.AudioSource.MIC, sampleRate,
                AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT, bufferSize);

        audio.startRecording();
        byte[] buffer = new byte[4096];
        do{
            int k=audio.read(buffer,0,buffer.length);
            if(k<=0)
                break;
            listener.onBytes(sampleRate, buffer, k);
        } while(running);
        audio.stop();
        synchronized (this){
            notifyAll();
        }
        audio.release();
    }

    public void finish() {
        synchronized (this){
            try {
                running=false;
                wait(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public static int[] findSampleRate()
    {
        // This is really ugly but this is another area where Android falls down.
        // I bet on the iPhone you can enumerate the supported sampling rates.
        // Actually they probably just tell you which are supported. Anyway, we shall try:
        //
        // 44100, 22050, 16000, 11025, 8000.
        int[] samplingRates = {44100, 22050, 16000, 11025, 8000};

        for (int samplingRate : samplingRates) {
            try {
                int min = AudioRecord.getMinBufferSize(samplingRate,
                        AudioFormat.CHANNEL_IN_MONO,
                        AudioFormat.ENCODING_PCM_16BIT);
                if (min < 4096)
                    min = 4096;
                AudioRecord record = new AudioRecord(MediaRecorder.AudioSource.MIC, samplingRate,
                        AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT, min);


                if (record.getState() == AudioRecord.STATE_INITIALIZED) {
                    int srate = record.getSampleRate();
                    Log.d("Recorder", "Audio recorder initialised at " + srate);
                    record.release();
                    return new int[]{srate, min};
                }
                record.release();
            } catch (IllegalArgumentException e) {
                // Meh. Try the next one.
            }
        }
        // None worked.
        return null;
    }
}
