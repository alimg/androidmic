package com.alimgokkaya.androidmic;

public interface RecordingListener {
    void onBytes(int freq, byte[] buffer, int numBytes);

}
