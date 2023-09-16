import type { Keplr } from "@keplr-wallet/types";

export {};

declare global {
  interface Window {
    keplr: Keplr;
  }
}