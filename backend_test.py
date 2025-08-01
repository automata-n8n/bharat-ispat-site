#!/usr/bin/env python3
"""
Backend Test Suite for Bharat Ispat Solution Website
Tests the static HTML website functionality and features
"""

import requests
import time
import json
import sys
from urllib.parse import urljoin
import subprocess
import os

class WebsiteTestSuite:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test(self, test_name, passed, message=""):
        """Log test results"""
        status = "✅ PASSED" if passed else "❌ FAILED"
        result = {
            "test": test_name,
            "status": status,
            "message": message
        }
        self.test_results.append(result)
        
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
            
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
    
    def test_server_availability(self):
        """Test if the website server is running and accessible"""
        try:
            response = requests.get(self.base_url, timeout=10)
            if response.status_code == 200:
                self.log_test("Server Availability", True, f"Server responding with status {response.status_code}")
                return True
            else:
                self.log_test("Server Availability", False, f"Server returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Server Availability", False, f"Server not accessible: {str(e)}")
            return False
    
    def test_html_structure(self):
        """Test HTML structure and essential elements"""
        try:
            response = requests.get(self.base_url, timeout=10)
            html_content = response.text
            
            # Check for essential HTML elements
            essential_elements = [
                ('<title>', 'Page title'),
                ('<meta name="description"', 'Meta description'),
                ('<nav', 'Navigation element'),
                ('id="home"', 'Home section'),
                ('id="about"', 'About section'),
                ('id="products"', 'Products section'),
                ('id="services"', 'Services section'),
                ('id="contact"', 'Contact section'),
                ('<form', 'Contact form'),
                ('<script>', 'JavaScript code')
            ]
            
            missing_elements = []
            for element, description in essential_elements:
                if element not in html_content:
                    missing_elements.append(description)
            
            if not missing_elements:
                self.log_test("HTML Structure", True, "All essential HTML elements found")
                return True
            else:
                self.log_test("HTML Structure", False, f"Missing elements: {', '.join(missing_elements)}")
                return False
                
        except Exception as e:
            self.log_test("HTML Structure", False, f"Error checking HTML structure: {str(e)}")
            return False
    
    def test_css_loading(self):
        """Test CSS and styling resources"""
        try:
            response = requests.get(self.base_url, timeout=10)
            html_content = response.text
            
            # Check for TailwindCSS CDN
            if 'tailwindcss.com' in html_content:
                self.log_test("CSS Loading - TailwindCSS", True, "TailwindCSS CDN found")
            else:
                self.log_test("CSS Loading - TailwindCSS", False, "TailwindCSS CDN not found")
            
            # Check for custom styles
            if 'styles.css' in html_content:
                # Test if styles.css is accessible
                styles_response = requests.get(urljoin(self.base_url, 'styles.css'), timeout=5)
                if styles_response.status_code == 200:
                    self.log_test("CSS Loading - Custom Styles", True, "Custom styles.css loaded successfully")
                else:
                    self.log_test("CSS Loading - Custom Styles", False, f"styles.css returned status {styles_response.status_code}")
            else:
                self.log_test("CSS Loading - Custom Styles", True, "No custom CSS file referenced (using inline styles)")
            
            return True
            
        except Exception as e:
            self.log_test("CSS Loading", False, f"Error checking CSS loading: {str(e)}")
            return False
    
    def test_javascript_loading(self):
        """Test JavaScript file loading"""
        try:
            # Test if script.js is accessible
            js_response = requests.get(urljoin(self.base_url, 'script.js'), timeout=5)
            if js_response.status_code == 200:
                js_content = js_response.text
                
                # Check for essential JavaScript functions
                essential_functions = [
                    'initNavigation',
                    'initContactForm',
                    'initProductCards',
                    'showProductModal',
                    'validateForm'
                ]
                
                missing_functions = []
                for func in essential_functions:
                    if func not in js_content:
                        missing_functions.append(func)
                
                if not missing_functions:
                    self.log_test("JavaScript Loading", True, "All essential JavaScript functions found")
                    return True
                else:
                    self.log_test("JavaScript Loading", False, f"Missing functions: {', '.join(missing_functions)}")
                    return False
            else:
                self.log_test("JavaScript Loading", False, f"script.js returned status {js_response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("JavaScript Loading", False, f"Error checking JavaScript loading: {str(e)}")
            return False
    
    def test_image_resources(self):
        """Test image loading and accessibility"""
        try:
            response = requests.get(self.base_url, timeout=10)
            html_content = response.text
            
            # Check for logo images
            logo_images = ['logo-full.jpeg', 'logo-icon.jpeg']
            logo_status = []
            
            for logo in logo_images:
                if logo in html_content:
                    try:
                        img_response = requests.get(urljoin(self.base_url, f'assets/images/{logo}'), timeout=5)
                        if img_response.status_code == 200:
                            logo_status.append(f"{logo}: ✅")
                        else:
                            logo_status.append(f"{logo}: ❌ (status {img_response.status_code})")
                    except:
                        logo_status.append(f"{logo}: ❌ (not accessible)")
                else:
                    logo_status.append(f"{logo}: ❌ (not referenced)")
            
            # Check for product images (sample check)
            product_images_found = html_content.count('assets/images/') > 2  # Should have multiple product images
            
            if all('✅' in status for status in logo_status) and product_images_found:
                self.log_test("Image Resources", True, f"Logo images and product images accessible. {'; '.join(logo_status)}")
                return True
            else:
                self.log_test("Image Resources", False, f"Some images not accessible. {'; '.join(logo_status)}")
                return False
                
        except Exception as e:
            self.log_test("Image Resources", False, f"Error checking image resources: {str(e)}")
            return False
    
    def test_navigation_structure(self):
        """Test navigation menu structure"""
        try:
            response = requests.get(self.base_url, timeout=10)
            html_content = response.text
            
            # Check for navigation links
            nav_links = ['#home', '#about', '#products', '#services', '#contact']
            missing_links = []
            
            for link in nav_links:
                if f'href="{link}"' not in html_content:
                    missing_links.append(link)
            
            # Check for mobile menu elements (updated IDs)
            mobile_elements = ['mobile-menu-btn', 'mobile-menu']
            missing_mobile = []
            
            for element in mobile_elements:
                if element not in html_content:
                    missing_mobile.append(element)
            
            if not missing_links and not missing_mobile:
                self.log_test("Navigation Structure", True, "All navigation links and mobile menu elements found")
                return True
            else:
                issues = []
                if missing_links:
                    issues.append(f"Missing links: {', '.join(missing_links)}")
                if missing_mobile:
                    issues.append(f"Missing mobile elements: {', '.join(missing_mobile)}")
                self.log_test("Navigation Structure", False, '; '.join(issues))
                return False
                
        except Exception as e:
            self.log_test("Navigation Structure", False, f"Error checking navigation structure: {str(e)}")
            return False
    
    def test_contact_form_structure(self):
        """Test contact form structure and elements"""
        try:
            response = requests.get(self.base_url, timeout=10)
            html_content = response.text
            
            # Check for form elements
            form_elements = [
                ('name="name"', 'Name field'),
                ('name="email"', 'Email field'),
                ('name="phone"', 'Phone field'),
                ('name="product"', 'Product dropdown'),
                ('name="message"', 'Message field'),
                ('type="submit"', 'Submit button'),
                ('id="contactForm"', 'Form ID')
            ]
            
            missing_elements = []
            for element, description in form_elements:
                if element not in html_content:
                    missing_elements.append(description)
            
            # Check for product options in dropdown
            product_options = ['MS TMT Bars', 'MS Pipes', 'Steel Billets', 'Aluminium Scrap']
            missing_products = []
            
            for product in product_options:
                if product not in html_content:
                    missing_products.append(product)
            
            if not missing_elements:
                if not missing_products:
                    self.log_test("Contact Form Structure", True, "All form elements and product options found")
                    return True
                else:
                    self.log_test("Contact Form Structure", True, f"Form complete but missing some products: {', '.join(missing_products)}")
                    return True
            else:
                self.log_test("Contact Form Structure", False, f"Missing form elements: {', '.join(missing_elements)}")
                return False
                
        except Exception as e:
            self.log_test("Contact Form Structure", False, f"Error checking contact form: {str(e)}")
            return False
    
    def test_product_showcase(self):
        """Test product showcase structure"""
        try:
            response = requests.get(self.base_url, timeout=10)
            html_content = response.text
            
            # Check for product categories
            product_categories = ['Mild Steel Products', 'Scrap Materials']
            category_found = []
            
            for category in product_categories:
                if category in html_content:
                    category_found.append(category)
            
            # Check for specific products
            key_products = ['MS TMT Bars', 'MS Sheets', 'Steel Billets', 'Aluminium Scrap', 'Copper Scrap']
            products_found = []
            
            for product in key_products:
                if product in html_content:
                    products_found.append(product)
            
            # Check for product interaction elements (updated to match actual HTML)
            interaction_elements = ['View Details', 'group bg-white rounded-2xl']
            interactions_found = []
            
            for element in interaction_elements:
                if element in html_content:
                    interactions_found.append(element)
            
            if len(category_found) >= 1 and len(products_found) >= 3 and len(interactions_found) >= 2:
                self.log_test("Product Showcase", True, f"Found {len(category_found)} categories, {len(products_found)} products, {len(interactions_found)} interaction elements")
                return True
            else:
                self.log_test("Product Showcase", False, f"Incomplete showcase: {len(category_found)} categories, {len(products_found)} products, {len(interactions_found)} interactions")
                return False
                
        except Exception as e:
            self.log_test("Product Showcase", False, f"Error checking product showcase: {str(e)}")
            return False
    
    def test_company_information(self):
        """Test company information and branding"""
        try:
            response = requests.get(self.base_url, timeout=10)
            html_content = response.text
            
            # Check for company details
            company_info = [
                'Bharat Ispat Solution',
                '20+ years',
                'SAIL',
                'TATA TISCON',
                'Noida',
                'business@bharatispats.com',
                '+91 120 6911055'
            ]
            
            info_found = []
            for info in company_info:
                if info in html_content:
                    info_found.append(info)
            
            # Check for professional sections
            sections = ['hero', 'about', 'services', 'contact']
            sections_found = []
            
            for section in sections:
                if f'id="{section}"' in html_content or f'class="{section}"' in html_content:
                    sections_found.append(section)
            
            if len(info_found) >= 5 and len(sections_found) >= 3:
                self.log_test("Company Information", True, f"Found {len(info_found)}/7 company details and {len(sections_found)}/4 sections")
                return True
            else:
                self.log_test("Company Information", False, f"Incomplete information: {len(info_found)}/7 details, {len(sections_found)}/4 sections")
                return False
                
        except Exception as e:
            self.log_test("Company Information", False, f"Error checking company information: {str(e)}")
            return False
    
    def test_seo_optimization(self):
        """Test SEO elements and meta tags"""
        try:
            response = requests.get(self.base_url, timeout=10)
            html_content = response.text
            
            # Check for SEO elements
            seo_elements = [
                ('<title>', 'Page title'),
                ('meta name="description"', 'Meta description'),
                ('meta name="keywords"', 'Meta keywords'),
                ('meta property="og:', 'Open Graph tags'),
                ('meta property="twitter:', 'Twitter cards'),
                ('rel="icon"', 'Favicon'),
                ('alt=', 'Image alt attributes')
            ]
            
            seo_score = 0
            missing_seo = []
            
            for element, description in seo_elements:
                if element in html_content:
                    seo_score += 1
                else:
                    missing_seo.append(description)
            
            # Check title length and content
            title_good = 'Steel Supplier' in html_content and len(html_content.split('<title>')[1].split('</title>')[0]) > 30
            
            if seo_score >= 6 and title_good:
                self.log_test("SEO Optimization", True, f"SEO score: {seo_score}/7 elements found")
                return True
            else:
                self.log_test("SEO Optimization", False, f"SEO score: {seo_score}/7. Missing: {', '.join(missing_seo)}")
                return False
                
        except Exception as e:
            self.log_test("SEO Optimization", False, f"Error checking SEO optimization: {str(e)}")
            return False
    
    def test_responsive_design_indicators(self):
        """Test responsive design indicators in HTML/CSS"""
        try:
            response = requests.get(self.base_url, timeout=10)
            html_content = response.text
            
            # Check for responsive design indicators
            responsive_indicators = [
                'viewport',
                'tailwindcss',
                'mobile',
                'hamburger',
                'responsive',
                'grid',
                'flex'
            ]
            
            indicators_found = []
            for indicator in responsive_indicators:
                if indicator.lower() in html_content.lower():
                    indicators_found.append(indicator)
            
            # Check for TailwindCSS responsive classes (sample)
            tailwind_responsive = ['md:', 'lg:', 'sm:', 'xl:']
            tailwind_found = []
            
            for tw_class in tailwind_responsive:
                if tw_class in html_content:
                    tailwind_found.append(tw_class)
            
            if len(indicators_found) >= 5 and len(tailwind_found) >= 2:
                self.log_test("Responsive Design Indicators", True, f"Found {len(indicators_found)} indicators and {len(tailwind_found)} Tailwind responsive classes")
                return True
            else:
                self.log_test("Responsive Design Indicators", False, f"Limited responsive indicators: {len(indicators_found)} general, {len(tailwind_found)} Tailwind")
                return False
                
        except Exception as e:
            self.log_test("Responsive Design Indicators", False, f"Error checking responsive design: {str(e)}")
            return False
    
    def test_performance_basics(self):
        """Test basic performance indicators"""
        try:
            start_time = time.time()
            response = requests.get(self.base_url, timeout=10)
            load_time = time.time() - start_time
            
            # Check response time
            if load_time < 2.0:
                time_status = "Excellent"
            elif load_time < 5.0:
                time_status = "Good"
            else:
                time_status = "Slow"
            
            # Check content size
            content_size = len(response.content)
            size_mb = content_size / (1024 * 1024)
            
            if size_mb < 1.0:
                size_status = "Optimal"
            elif size_mb < 3.0:
                size_status = "Acceptable"
            else:
                size_status = "Large"
            
            # Check for performance optimizations
            optimizations = []
            if 'lazy' in response.text.lower():
                optimizations.append("Lazy loading")
            if 'defer' in response.text.lower():
                optimizations.append("Deferred scripts")
            if 'async' in response.text.lower():
                optimizations.append("Async scripts")
            
            performance_good = load_time < 5.0 and size_mb < 3.0
            
            if performance_good:
                self.log_test("Performance Basics", True, f"Load time: {load_time:.2f}s ({time_status}), Size: {size_mb:.2f}MB ({size_status}), Optimizations: {len(optimizations)}")
                return True
            else:
                self.log_test("Performance Basics", False, f"Performance issues - Load time: {load_time:.2f}s, Size: {size_mb:.2f}MB")
                return False
                
        except Exception as e:
            self.log_test("Performance Basics", False, f"Error checking performance: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🚀 Starting Bharat Ispat Solution Website Test Suite")
        print("=" * 60)
        
        # Run all tests
        tests = [
            self.test_server_availability,
            self.test_html_structure,
            self.test_css_loading,
            self.test_javascript_loading,
            self.test_image_resources,
            self.test_navigation_structure,
            self.test_contact_form_structure,
            self.test_product_showcase,
            self.test_company_information,
            self.test_seo_optimization,
            self.test_responsive_design_indicators,
            self.test_performance_basics
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                self.log_test(test.__name__, False, f"Test execution error: {str(e)}")
            print()  # Add spacing between tests
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary report"""
        print("=" * 60)
        print("📊 TEST SUMMARY REPORT")
        print("=" * 60)
        
        total_tests = self.passed_tests + self.failed_tests
        pass_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.failed_tests} ❌")
        print(f"Pass Rate: {pass_rate:.1f}%")
        print()
        
        # Overall status
        if pass_rate >= 90:
            status = "🟢 EXCELLENT"
        elif pass_rate >= 75:
            status = "🟡 GOOD"
        elif pass_rate >= 50:
            status = "🟠 NEEDS IMPROVEMENT"
        else:
            status = "🔴 CRITICAL ISSUES"
        
        print(f"Overall Status: {status}")
        print()
        
        # Failed tests details
        if self.failed_tests > 0:
            print("❌ FAILED TESTS:")
            for result in self.test_results:
                if "FAILED" in result["status"]:
                    print(f"  • {result['test']}: {result['message']}")
            print()
        
        # Recommendations
        print("💡 RECOMMENDATIONS:")
        if self.failed_tests == 0:
            print("  • Website is fully functional and ready for production")
            print("  • Consider adding backend form processing")
            print("  • Monitor performance in production environment")
        else:
            print("  • Address failed test issues before production deployment")
            print("  • Verify all resources are properly accessible")
            print("  • Test functionality in different browsers")
        
        print("=" * 60)
        
        # Return overall success status
        return pass_rate >= 75

def main():
    """Main test execution"""
    # Check if server is running, if not start it
    try:
        requests.get("http://localhost:8000", timeout=2)
        print("✅ Server already running on port 8000")
    except:
        print("🚀 Starting HTTP server on port 8000...")
        # Start server in background
        subprocess.Popen(['python3', '-m', 'http.server', '8000'], 
                        cwd='/app', 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        time.sleep(3)  # Wait for server to start
    
    # Run tests
    test_suite = WebsiteTestSuite()
    success = test_suite.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()