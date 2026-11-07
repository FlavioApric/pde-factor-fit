#!/usr/bin/env bash
# Fails if internal project vocabulary leaks into the manuscripts (ledger labels, phase names, notes).
# Usage: bash paper/tools/hygiene.sh   (from the repository root)
set -u
cd "$(dirname "$0")/.." || exit 2
pattern='\b(FASI|HANDOFF|ledger|Phase ?[0-9]|PHASE|T[0-9]{1,3}\b|C3-|C12-|P[0-9]-T|S4ID|S4T|OPF|OPA-|R2-T|II-T|AI agent|Lean 4|no ML rule|ProblemaBase|PDEFactorML|TODO|XXX)'
hits=$(grep -n -E "$pattern" A_user_structure/*.tex B_proposed_structure/*.tex shared/*.tex shared/sections/*.tex | grep -v usepackage || true)
if [ -n "$hits" ]; then
  echo "Internal vocabulary found in the manuscripts:"; echo "$hits"; exit 1
fi
echo "hygiene: clean"
