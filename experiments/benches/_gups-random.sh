#!/bin/bash

THREADS=16
UPDATES=1000000000
DATASIZE=8

# /users/zackng03/IDT/experiments/workloads/
GUPSPATH="/users/zackng03/IDT/experiments/workloads/GUPS"

if [[ "${BENCH_SIZE}" == "small" ]]; then
	BENCH_RUN+="numactl -N0 -c0 -- "$GUPSPATH/gups-random" $THREADS $UPDATES 34 $DATASIZE 34"
elif [[ "${BENCH_SIZE}" == "large" ]]; then
	BENCH_RUN+="numactl -N0 -c0 -- "$GUPSPATH/gups-random" $THREADS $UPDATES 37 $DATASIZE 37"
else
	err "ERROR: Retry with available SIZE. refer to benches/_gups-random.sh"
	exit -1
fi

export BENCH_RUN
export BENCH_NAME="gups-random"
