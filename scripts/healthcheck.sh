#!/usr/bin/env bash
set -euo pipefail

SERVER="${1:-localhost}"
printf "CostForge Healthcheck\nTarget: %s\n\n" "$SERVER"

check_service() {
    local name="$1"
    local url="$2"
    local expected="${3:-}"

    if [[ -n "$expected" ]]; then
        if curl -sf "$url" | grep -q "$expected"; then
            printf "  ✅ %s\n" "$name"
            return 0
        fi
    else
        if curl -sf "$url" >/dev/null; then
            printf "  ✅ %s\n" "$name"
            return 0
        fi
    fi
    printf "  ❌ %s\n" "$name"
    return 1
}

FAILED=0

echo "Backend:"
check_service "CostForge Backend" "http://$SERVER:8000/healthz" "ok" || FAILED=1

echo ""
echo "Frontend:"
check_service "CostForge Frontend" "http://$SERVER:8090/" "CostForge" || FAILED=1

echo ""
if [[ $FAILED -eq 0 ]]; then
    echo "🎉 All services healthy!"
    exit 0
else
    echo "⚠️  Some services are down"
    exit 1
fi