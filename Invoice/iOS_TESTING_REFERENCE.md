# iOS Testing Quick Reference
# ==========================

## Quick Start
1. Run: `ios_test_setup.bat`
2. Note the IP address shown
3. On iOS Safari, go to: `http://[IP]:5000`

## URLs to Test
- Main App: `http://[YOUR_IP]:5000`
- Mobile Interface: `http://[YOUR_IP]:5000/mobile`
- API Endpoint: `http://[YOUR_IP]:5000/api/upload`

## iOS Testing Checklist
✓ Camera access granted
✓ Photo library access works
✓ File upload successful
✓ Touch interface responsive
✓ Receipt generation works
✓ File downloads work

## Common Issues
**Can't connect**: Check firewall, same WiFi network
**Camera not working**: Grant Safari camera permission
**Slow upload**: Use smaller test images
**Download fails**: Try different file format

## Test Files Location
- Sample images in current directory
- Generated receipts in current directory
- Uploaded files in `uploads/` folder

## Mobile Features to Test
1. Camera capture
2. Photo library selection
3. Touch-friendly interface
4. Portrait/landscape modes
5. File drag & drop
6. Form editing
7. Receipt download

## Performance Tips
- Use images under 5MB for testing
- Ensure strong WiFi signal
- Close other apps on iOS device
- Test with different image formats (JPG, PNG, PDF)

## Security Notes
- Only for local network testing
- Don't expose to internet
- Change secret key for production
- HTTPS required for production camera access
