"""
Online No. Positioning Fix Summary
==================================

BEFORE THE FIX:
- Fixed x-coordinate of 200 was used for all values
- "Online No." value appeared too far to the right
- Layout: [Label at x=50] --------gap-------- [Value at x=200]

AFTER THE FIX:
- Dynamic positioning based on actual label width
- Value appears right after the label with proper spacing
- Layout: [Label at x=50][small gap][Value at calculated position]

TECHNICAL CHANGES:
1. Calculate label width using textbbox()
2. Position value at: label_start + label_width + small_gap
3. Applied to both printreceipt.py and printreceipt copy.py

PAYMENT METHOD LABELS:
- CASH: "Reference No."
- CHEQUE: "Cheque No." 
- ONLINE: "Online No."

The fix ensures proper spacing regardless of which label is used.
"""
