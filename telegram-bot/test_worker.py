"""
Test script untuk Jhopan API
Untuk memastikan Worker sudah jalan dengan benar sebelum run bot
"""

import requests
import sys
from typing import Dict, Any


class JhopanTester:
    def __init__(self, worker_domain: str):
        self.worker_domain = worker_domain
        self.base_url = f"https://{worker_domain}"
        self.api_url = f"{self.base_url}/api/v1/sub"
        self.results = []
    
    def print_header(self, text: str):
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)
    
    def print_result(self, name: str, status: bool, message: str = ""):
        icon = "✅" if status else "❌"
        self.results.append((name, status))
        print(f"{icon} {name}")
        if message:
            print(f"   {message}")
    
    def test_worker_alive(self) -> bool:
        """Test if worker is responding"""
        try:
            response = requests.get(self.base_url, timeout=10)
            self.print_result(
                "Worker Alive",
                response.status_code in [200, 301, 302],
                f"Status: {response.status_code}"
            )
            return True
        except Exception as e:
            self.print_result("Worker Alive", False, f"Error: {e}")
            return False
    
    def test_api_endpoint(self) -> bool:
        """Test API endpoint"""
        try:
            response = requests.get(
                self.api_url,
                params={"limit": 1, "format": "raw"},
                timeout=15
            )
            success = response.status_code == 200
            self.print_result(
                "API Endpoint",
                success,
                f"Status: {response.status_code}, Length: {len(response.text)}"
            )
            
            if success and response.text:
                print(f"   Sample: {response.text[:100]}...")
            
            return success
        except Exception as e:
            self.print_result("API Endpoint", False, f"Error: {e}")
            return False
    
    def test_country_filter(self) -> bool:
        """Test country filter"""
        try:
            response = requests.get(
                self.api_url,
                params={"cc": "ID", "limit": 2, "format": "raw"},
                timeout=15
            )
            success = response.status_code == 200 and "ID" in response.text
            self.print_result(
                "Country Filter (ID)",
                success,
                f"Status: {response.status_code}"
            )
            return success
        except Exception as e:
            self.print_result("Country Filter", False, f"Error: {e}")
            return False
    
    def test_protocol_filter(self) -> bool:
        """Test protocol filter"""
        protocols = ["vless", "trojan", "ss"]
        all_success = True
        
        for proto in protocols:
            try:
                response = requests.get(
                    self.api_url,
                    params={"vpn": proto, "limit": 1, "format": "raw"},
                    timeout=15
                )
                success = response.status_code == 200
                self.print_result(
                    f"Protocol: {proto.upper()}",
                    success,
                    f"Status: {response.status_code}"
                )
                all_success = all_success and success
            except Exception as e:
                self.print_result(f"Protocol: {proto.upper()}", False, f"Error: {e}")
                all_success = False
        
        return all_success
    
    def test_port_filter(self) -> bool:
        """Test port filter"""
        try:
            response = requests.get(
                self.api_url,
                params={"port": "443", "limit": 1, "format": "raw"},
                timeout=15
            )
            success = response.status_code == 200 and ":443" in response.text
            self.print_result(
                "Port Filter (443)",
                success,
                f"Status: {response.status_code}"
            )
            return success
        except Exception as e:
            self.print_result("Port Filter", False, f"Error: {e}")
            return False
    
    def test_format_outputs(self) -> bool:
        """Test different output formats"""
        formats = {
            "raw": lambda t: "://" in t,
            "v2ray": lambda t: len(t) > 50,  # Base64 should be long
            "clash": lambda t: "proxies:" in t or "proxy-groups:" in t,
        }
        
        all_success = True
        for fmt, validator in formats.items():
            try:
                response = requests.get(
                    self.api_url,
                    params={"format": fmt, "limit": 2},
                    timeout=20
                )
                success = response.status_code == 200 and validator(response.text)
                self.print_result(
                    f"Format: {fmt}",
                    success,
                    f"Status: {response.status_code}, Valid: {validator(response.text)}"
                )
                all_success = all_success and success
            except Exception as e:
                self.print_result(f"Format: {fmt}", False, f"Error: {e}")
                all_success = False
        
        return all_success
    
    def test_myip_endpoint(self) -> bool:
        """Test myip endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/myip", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.print_result(
                    "MyIP Endpoint",
                    True,
                    f"IP: {data.get('ip', 'N/A')}, Colo: {data.get('colo', 'N/A')}"
                )
            else:
                self.print_result("MyIP Endpoint", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.print_result("MyIP Endpoint", False, f"Error: {e}")
            return False
    
    def test_performance(self) -> bool:
        """Test response time"""
        try:
            import time
            start = time.time()
            response = requests.get(
                self.api_url,
                params={"limit": 5, "format": "raw"},
                timeout=15
            )
            elapsed = time.time() - start
            
            success = response.status_code == 200 and elapsed < 5
            self.print_result(
                "Performance",
                success,
                f"Response time: {elapsed:.2f}s (target: < 5s)"
            )
            return success
        except Exception as e:
            self.print_result("Performance", False, f"Error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        self.print_header("🧪 Nautica Worker Test Suite")
        print(f"\nTesting Worker: {self.worker_domain}")
        print(f"API URL: {self.api_url}\n")
        
        # Basic tests
        self.print_header("1️⃣  Basic Connectivity")
        self.test_worker_alive()
        self.test_api_endpoint()
        self.test_myip_endpoint()
        
        # Filter tests
        self.print_header("2️⃣  Filter Tests")
        self.test_country_filter()
        self.test_protocol_filter()
        self.test_port_filter()
        
        # Format tests
        self.print_header("3️⃣  Format Output Tests")
        self.test_format_outputs()
        
        # Performance
        self.print_header("4️⃣  Performance Test")
        self.test_performance()
        
        # Summary
        self.print_header("📊 Test Summary")
        passed = sum(1 for _, status in self.results if status)
        total = len(self.results)
        percentage = (passed / total * 100) if total > 0 else 0
        
        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {percentage:.1f}%")
        
        if percentage == 100:
            print("\n✅ All tests passed! Worker is ready to use.")
            print("   You can now run the Telegram bot with confidence.")
        elif percentage >= 80:
            print("\n⚠️  Most tests passed, but some failed.")
            print("   Check failed tests above and fix if necessary.")
        else:
            print("\n❌ Many tests failed!")
            print("   Please check your worker configuration.")
        
        print("\n" + "=" * 60)
        return percentage == 100


def main():
    print("""
╔══════════════════════════════════════════╗
║                                          ║
║      🧪 JHOPAN WORKER TEST SUITE 🧪      ║
║                                          ║
╚══════════════════════════════════════════╝
""")
    
    # Get worker domain
    if len(sys.argv) > 1:
        worker_domain = sys.argv[1]
    else:
        worker_domain = input("Enter Worker Domain (e.g., jhopan.workers.dev): ").strip()
        
        if not worker_domain:
            print("❌ Error: Worker domain is required!")
            print("\nUsage: python test_worker.py <worker-domain>")
            print("Example: python test_worker.py jhopan.workers.dev")
            sys.exit(1)
    
    # Remove https:// if present
    worker_domain = worker_domain.replace("https://", "").replace("http://", "")
    
    # Run tests
    tester = JhopanTester(worker_domain)
    success = tester.run_all_tests()
    
    # Exit code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
