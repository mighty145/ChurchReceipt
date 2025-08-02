#!/usr/bin/env python3
"""
Mobile Compatibility Test Script for Church Invoice App

This script tests the mobile compatibility features of the Flask web application.
"""

import requests
import json
import os
import sys
from pathlib import Path

def test_mobile_endpoints():
    """Test mobile-specific endpoints"""
    base_url = "http://localhost:5000"
    
    print("🔍 Testing Mobile Compatibility...")
    print("=" * 50)
    
    tests = []
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            tests.append({
                'name': 'Health Check',
                'status': '✅ PASS' if data.get('mobile_compatible') and data.get('ios_compatible') and data.get('android_compatible') else '❌ FAIL',
                'details': f"Mobile: {data.get('mobile_compatible')}, iOS: {data.get('ios_compatible')}, Android: {data.get('android_compatible')}"
            })
        else:
            tests.append({'name': 'Health Check', 'status': '❌ FAIL', 'details': f"HTTP {response.status_code}"})
    except Exception as e:
        tests.append({'name': 'Health Check', 'status': '❌ FAIL', 'details': str(e)})
    
    # Test 2: Mobile interface
    try:
        response = requests.get(f"{base_url}/mobile", timeout=5)
        mobile_features = [
            'viewport', 'apple-mobile-web-app', 'theme-color', 
            'manifest.json', '-webkit-', 'touch'
        ]
        
        content = response.text.lower()
        detected_features = [feature for feature in mobile_features if feature in content]
        
        tests.append({
            'name': 'Mobile Interface',
            'status': '✅ PASS' if len(detected_features) >= 4 else '❌ FAIL',
            'details': f"Detected features: {', '.join(detected_features)}"
        })
    except Exception as e:
        tests.append({'name': 'Mobile Interface', 'status': '❌ FAIL', 'details': str(e)})
    
    # Test 3: PWA Manifest
    try:
        response = requests.get(f"{base_url}/manifest.json", timeout=5)
        if response.status_code == 200:
            manifest = response.json()
            required_fields = ['name', 'start_url', 'display', 'icons']
            has_required = all(field in manifest for field in required_fields)
            
            tests.append({
                'name': 'PWA Manifest',
                'status': '✅ PASS' if has_required else '❌ FAIL',
                'details': f"Required fields: {has_required}, Display: {manifest.get('display')}"
            })
        else:
            tests.append({'name': 'PWA Manifest', 'status': '❌ FAIL', 'details': f"HTTP {response.status_code}"})
    except Exception as e:
        tests.append({'name': 'PWA Manifest', 'status': '❌ FAIL', 'details': str(e)})
    
    # Test 4: Service Worker
    try:
        response = requests.get(f"{base_url}/static/sw.js", timeout=5)
        if response.status_code == 200:
            sw_content = response.text.lower()
            sw_features = ['cache', 'install', 'fetch', 'activate']
            detected_sw_features = [feature for feature in sw_features if feature in sw_content]
            
            tests.append({
                'name': 'Service Worker',
                'status': '✅ PASS' if len(detected_sw_features) >= 3 else '❌ FAIL',
                'details': f"SW features: {', '.join(detected_sw_features)}"
            })
        else:
            tests.append({'name': 'Service Worker', 'status': '❌ FAIL', 'details': f"HTTP {response.status_code}"})
    except Exception as e:
        tests.append({'name': 'Service Worker', 'status': '❌ FAIL', 'details': str(e)})
    
    # Display results
    print("\n📊 Test Results:")
    print("-" * 50)
    
    for test in tests:
        print(f"{test['status']} {test['name']}")
        print(f"    {test['details']}")
        print()
    
    # Summary
    passed = sum(1 for test in tests if '✅' in test['status'])
    total = len(tests)
    
    print("📈 Summary:")
    print(f"   Passed: {passed}/{total}")
    print(f"   Success Rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All mobile compatibility tests passed!")
        print("   Your app is ready for iOS and Android!")
    elif passed >= total * 0.75:
        print("\n⚠️  Most tests passed, but some improvements needed.")
    else:
        print("\n❌ Several tests failed. Mobile compatibility needs attention.")
    
    return passed == total

def check_file_features():
    """Check file-based mobile features"""
    print("\n🔍 Checking File-Based Mobile Features...")
    print("=" * 50)
    
    # Check mobile HTML file
    mobile_html_path = Path("mobile_upload.html")
    if mobile_html_path.exists():
        with open(mobile_html_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        ios_features = [
            'apple-mobile-web-app', 'user-scalable=no', '-webkit-',
            'capture="environment"', 'haptic', 'orientation'
        ]
        android_features = [
            'android', 'theme-color', 'mobile-web-app', 
            'accept="image/*"', 'navigator.vibrate'
        ]
        
        ios_detected = [f for f in ios_features if f in content]
        android_detected = [f for f in android_features if f in content]
        
        print(f"✅ iOS Features Detected ({len(ios_detected)}/6):")
        for feature in ios_detected:
            print(f"   - {feature}")
        
        print(f"\n✅ Android Features Detected ({len(android_detected)}/5):")
        for feature in android_detected:
            print(f"   - {feature}")
        
        return len(ios_detected) >= 4 and len(android_detected) >= 3
    else:
        print("❌ mobile_upload.html not found!")
        return False

if __name__ == "__main__":
    print("🚀 Church Invoice App - Mobile Compatibility Test")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        print("✅ Flask server is running")
    except:
        print("❌ Flask server is not running!")
        print("   Please start the server with: python web_invoice_app.py")
        sys.exit(1)
    
    # Run tests
    endpoint_tests_passed = test_mobile_endpoints()
    file_tests_passed = check_file_features()
    
    # Final assessment
    print("\n" + "=" * 60)
    if endpoint_tests_passed and file_tests_passed:
        print("🎉 OVERALL: MOBILE COMPATIBILITY EXCELLENT!")
        print("   Your app is fully compatible with iOS and Android!")
    elif endpoint_tests_passed or file_tests_passed:
        print("⚠️  OVERALL: MOBILE COMPATIBILITY GOOD")
        print("   Some minor improvements could be made.")
    else:
        print("❌ OVERALL: MOBILE COMPATIBILITY NEEDS WORK")
        print("   Several issues need to be addressed.")
