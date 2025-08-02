# iOS Mobile Testing Guide for Invoice Analyzer Web App
# ==================================================

"""
Complete guide for testing the Flask web application on iOS devices.
This covers both the main web app and the standalone mobile interface.
"""

def get_testing_instructions():
    return """
iOS MOBILE TESTING GUIDE
========================

PREREQUISITES:
--------------
1. Ensure your Flask app is running on your computer
2. Make sure your iOS device and computer are on the same network
3. Find your computer's local IP address

STEP 1: Start the Flask Application
----------------------------------
1. Open Terminal/Command Prompt on your computer
2. Navigate to the project directory:
   cd "c:\\Users\\might\\Projects\\ChruchProject\\Invoice"

3. Start the Flask app:
   py web_invoice_app.py

4. You should see output like:
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:5000
   * Running on http://[YOUR_IP]:5000

STEP 2: Find Your Computer's IP Address
---------------------------------------
Windows:
- Open Command Prompt
- Type: ipconfig
- Look for "IPv4 Address" under your active network adapter
- Example: 192.168.1.100

Mac:
- System Preferences > Network > Select your connection
- Note the IP address shown
- Example: 192.168.1.100

STEP 3: Test on iOS Device
-------------------------
Option A: Main Web Application
1. Open Safari on your iOS device
2. Go to: http://[YOUR_IP]:5000
   Example: http://192.168.1.100:5000

3. You should see the upload interface
4. Test file upload using camera or photo library
5. Verify the analysis and receipt generation features

Option B: Standalone Mobile Interface
1. Open Safari on your iOS device
2. Go to: http://[YOUR_IP]:5000/static/mobile_upload.html
   (Note: You may need to serve mobile_upload.html through Flask)

STEP 4: iOS-Specific Testing Checklist
--------------------------------------
Camera Access:
✓ Test camera capture functionality
✓ Verify photo library access
✓ Check file upload from both sources

Touch Interface:
✓ Test touch interactions and gestures
✓ Verify drag-and-drop file upload
✓ Check form field editing on mobile

Performance:
✓ Test file upload speed
✓ Verify image processing doesn't timeout
✓ Check responsiveness on different screen sizes

Browser Compatibility:
✓ Test in Safari (primary)
✓ Test in Chrome for iOS (secondary)
✓ Verify all features work in both browsers

STEP 5: Common iOS Testing Issues & Solutions
--------------------------------------------
Issue: "Cannot connect to server"
Solution: 
- Check firewall settings on your computer
- Ensure both devices are on same WiFi network
- Try disabling Windows Firewall temporarily

Issue: Camera not working
Solution:
- Safari will prompt for camera permission
- Go to Settings > Safari > Camera & Microphone > Allow

Issue: File upload fails
Solution:
- Check file size (max 16MB)
- Verify file format (jpg, png, pdf supported)
- Try smaller test images first

Issue: Slow performance
Solution:
- Use smaller image files for testing
- Ensure strong WiFi connection
- Close other apps on iOS device

STEP 6: Advanced Testing Scenarios
---------------------------------
1. Receipt Generation Flow:
   - Upload invoice image
   - Verify extracted data accuracy
   - Edit fields if needed
   - Generate receipt
   - Download receipt files

2. API Testing (for mobile app integration):
   - Test POST /api/upload endpoint
   - Verify JSON response format
   - Check error handling

3. Multi-format Testing:
   - Test JPG uploads
   - Test PNG uploads  
   - Test PDF uploads
   - Verify each format processes correctly

STEP 7: Production Deployment Considerations
-------------------------------------------
For real mobile app deployment:
- Use HTTPS (required for camera access in production)
- Configure proper domain name
- Set up SSL certificates
- Consider using ngrok for external testing
- Implement proper authentication if needed

TROUBLESHOOTING COMMANDS:
------------------------
Check if Flask is running:
netstat -ano | findstr :5000

Check firewall status:
netsh advfirewall show allprofiles

Test network connectivity:
ping [YOUR_IP]

SECURITY NOTES:
--------------
- The current setup is for local testing only
- Don't expose this to the internet without proper security
- Change the Flask secret key before production use
- Implement authentication for production deployment
"""

def get_mobile_specific_features():
    return """
MOBILE-SPECIFIC FEATURES TO TEST:
=================================

1. Camera Integration:
   - Tap to take photo directly
   - Access photo library
   - Image preview before upload

2. Touch Optimizations:
   - Large touch targets
   - Swipe gestures
   - Pinch to zoom on images

3. Responsive Design:
   - Portrait and landscape modes
   - Different screen sizes (iPhone SE to iPhone Pro Max)
   - Proper scaling of UI elements

4. File Handling:
   - Direct camera capture
   - Photo library selection
   - Drag and drop (iOS 11+)

5. Progressive Web App Features:
   - Add to home screen capability
   - Offline functionality (if implemented)
   - Push notifications (if needed)
"""

def get_testing_checklist():
    return """
iOS TESTING CHECKLIST:
=====================

PRE-TESTING:
□ Flask app is running
□ Computer and iOS device on same network
□ IP address identified
□ Firewall configured properly

BASIC FUNCTIONALITY:
□ Can access web app from iOS Safari
□ Upload interface loads correctly
□ Camera permission granted
□ Photo library access works
□ File upload completes successfully

INVOICE ANALYSIS:
□ Image analysis completes
□ Extracted data displays correctly
□ All form fields are editable
□ Data validation works

RECEIPT GENERATION:
□ Receipt generates successfully
□ Multiple formats available (JPG, PDF)
□ Download links work
□ Files download to iOS device

USER EXPERIENCE:
□ Interface is touch-friendly
□ Text is readable on mobile
□ Buttons are easily tappable
□ Loading states are clear
□ Error messages are helpful

PERFORMANCE:
□ App loads quickly
□ File uploads don't timeout
□ Image processing completes in reasonable time
□ No memory issues or crashes

EDGE CASES:
□ Large file uploads
□ Poor network conditions
□ Invalid file formats
□ Server errors handled gracefully
"""

if __name__ == "__main__":
    print("=== iOS Mobile Testing Guide ===")
    print(get_testing_instructions())
    print("\n" + "="*50 + "\n")
    print(get_mobile_specific_features())
    print("\n" + "="*50 + "\n")
    print(get_testing_checklist())
