# tests/load/latency_test.py
"""
Prueba de latencia simple sin dependencias externas.

Ejecutar con:
    python tests/load/latency_test.py
"""
import urllib.request
import time
import statistics

ENDPOINTS = [
    ("Manga Health", "https://inku-manga-service.onrender.com/api/health"),
    ("Auth Health", "https://inku-auth-service.onrender.com/health"),
    ("List Health", "https://inku-list-service.onrender.com/health"),
    ("Mangas List", "https://inku-manga-service.onrender.com/api/mangas"),
    ("Public Lists", "https://inku-list-service.onrender.com/api/lists/public"),
]

def measure_latency(url: str, num_requests: int = 10) -> dict:
    """Mide la latencia de un endpoint."""
    times = []
    errors = 0
    
    for i in range(num_requests):
        try:
            start = time.time()
            with urllib.request.urlopen(url, timeout=30) as response:
                response.read()
            end = time.time()
            latency_ms = (end - start) * 1000
            times.append(latency_ms)
            print(f"  Request {i+1}/{num_requests}: {latency_ms:.0f}ms")
        except Exception as e:
            errors += 1
            print(f"  Request {i+1}/{num_requests}: ERROR - {e}")
    
    if times:
        return {
            "min": min(times),
            "max": max(times),
            "avg": statistics.mean(times),
            "p50": statistics.median(times),
            "errors": errors,
            "success_rate": (num_requests - errors) / num_requests * 100
        }
    return {"errors": errors, "success_rate": 0}

def main():
    print("=" * 60)
    print("🚀 PRUEBA DE LATENCIA - INKU SERVICES")
    print("=" * 60)
    
    results = {}
    
    for name, url in ENDPOINTS:
        print(f"\n📊 Testing: {name}")
        print(f"   URL: {url}")
        print("-" * 40)
        results[name] = measure_latency(url, num_requests=5)
    
    # Resumen
    print("\n" + "=" * 60)
    print("📈 RESUMEN DE RESULTADOS")
    print("=" * 60)
    print(f"{'Endpoint':<20} {'Min':>8} {'Avg':>8} {'Max':>8} {'Success':>10}")
    print("-" * 60)
    
    for name, data in results.items():
        if "avg" in data:
            print(f"{name:<20} {data['min']:>7.0f}ms {data['avg']:>7.0f}ms {data['max']:>7.0f}ms {data['success_rate']:>9.0f}%")
        else:
            print(f"{name:<20} {'N/A':>8} {'N/A':>8} {'N/A':>8} {data['success_rate']:>9.0f}%")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
