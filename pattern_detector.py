import pandas as pd

def detect_double_top(df, threshold=0.005):
    """Çift Tepe Formasyonu tespiti"""
    signals = []
    for i in range(2, len(df) - 2):
        p1 = df['high'].iloc[i - 2]
        p2 = df['high'].iloc[i]
        p3 = df['high'].iloc[i + 2]
        if abs(p1 - p2) / p1 < threshold and p2 > df['high'].iloc[i - 1] and p2 > df['high'].iloc[i + 1] and p2 > p3:
            signals.append((df['time'].iloc[i], "double_top"))
    return signals

def detect_double_bottom(df, threshold=0.005):
    """Çift Dip Formasyonu tespiti"""
    signals = []
    for i in range(2, len(df) - 2):
        p1 = df['low'].iloc[i - 2]
        p2 = df['low'].iloc[i]
        p3 = df['low'].iloc[i + 2]
        if abs(p1 - p2) / p1 < threshold and p2 < df['low'].iloc[i - 1] and p2 < df['low'].iloc[i + 1] and p2 < p3:
            signals.append((df['time'].iloc[i], "double_bottom"))
    return signals

def detect_head_and_shoulders(df, threshold=0.005):
    """OBO (Head and Shoulders) tespiti - basit yaklaşım"""
    signals = []
    for i in range(3, len(df) - 3):
        l = df['high'].iloc[i - 3:i + 4].values
        if l[1] < l[2] and l[2] > l[3] and l[0] < l[2] and l[4] < l[2]:
            if abs(l[1] - l[3]) / l[2] < threshold:
                signals.append((df['time'].iloc[i], "head_and_shoulders"))
    return signals

def detect_patterns(df):
    """Tüm formasyonları kontrol eder"""
    all_signals = []
    all_signals.extend(detect_double_top(df))
    all_signals.extend(detect_double_bottom(df))
    all_signals.extend(detect_head_and_shoulders(df))
    return all_signals
