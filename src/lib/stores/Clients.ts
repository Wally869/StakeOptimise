import { writable, type Writable } from 'svelte/store';
import type { Keplr } from '@keplr-wallet/types';
import type { ReadClient } from '$lib/network-utils';
import type { SigningStargateClient, StargateClient } from '@cosmjs/stargate';

export const READ_CLIENT: Writable<null | ReadClient> = writable(null);
export const WRITE_CLIENT: Writable<null | Keplr> = writable(null);

export const STARGATE_SIGNING_CLIENT: Writable<null | SigningStargateClient> = writable(null);

export const USER_ADDRESS: Writable<string | null> = writable(null);