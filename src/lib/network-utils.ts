import { QueryClient, StargateClient, setupGovExtension, type GovExtension, setupStakingExtension, type StakingExtension, type BankExtension, setupBankExtension, type Coin, SigningStargateClient, GasPrice } from "@cosmjs/stargate";
import { HttpBatchClient, Tendermint37Client } from "@cosmjs/tendermint-rpc"
import type { Keplr } from '@keplr-wallet/types';
import type { StakingTarget, Validator } from "./types/pytypes";

import { MsgDelegate } from 'cosmjs-types/cosmos/staking/v1beta1/tx';
import { READ_CLIENT, STARGATE_SIGNING_CLIENT, USER_ADDRESS } from "./stores/Clients";
import { COSMOS_TESTNET } from "./settings/cosmos_testnet";

export const HACKATHON_MEMO = "aez_wally869_stake-optimizer"

export type ReadClient = QueryClient & StakingExtension & BankExtension;

export interface TokenData {
    base: string
    denom: string
    decimals: number
}

export interface Fees {
    denom: string
    fixed_min_gas_price: number
}

export interface NetworkSettings {
    chain_id: string
    rpc: string
    token: TokenData
    fees: Fees
}


export async function create_client(chain_rpc: string): Promise<ReadClient> {
    const batch_client = new HttpBatchClient(chain_rpc)
    const tendermint = await Tendermint37Client.create(batch_client);

    //const stargate_client = await StargateClient.create(tendermint);
    const query_client = QueryClient.withExtensions(
        tendermint, setupStakingExtension, setupBankExtension
    );

    return query_client;
}


export async function get_validator_data(client: ReadClient): Promise<Validator[]> {
    let validators_data: Validator[] = [];

    let next_key: Uint8Array | undefined;
    while (true) {
        //console.log("querying rpc");
        let temp;
        if (next_key) {
            temp = await client.staking.validators("BOND_STATUS_BONDED", next_key);
        } else {
            temp = await client.staking.validators("BOND_STATUS_BONDED");
        }

        validators_data = validators_data.concat(
            ...temp.validators.map(
                (val) => {
                    let comm: number = 0.0;
                    if (val.commission?.commissionRates?.rate) {
                        comm = parseFloat(val.commission?.commissionRates?.rate);
                    } else {
                        comm = 0.0;
                    }

                    return {
                        "moniker": val.description?.moniker ?? "",
                        "address": val.operatorAddress,
                        "curr_stake": parseFloat(val.tokens) / Math.pow(10, COSMOS_TESTNET.token.decimals),
                        "commission_rate": comm //(val.commission?.commissionRates?.rate ? val.commission?.commissionRates?.rate? : 0.0) 
                    }
                }
            )
        )

        if (temp.pagination?.total && temp.pagination?.total.lessThan(100)) {
            break;
        } else {
            next_key = temp.pagination?.nextKey;
        }

        /*
        if (temp.pagination?.nextKey.length == 0) {
            break;
        } else {
            next_key = temp.pagination?.nextKey;
        }
        */
    }

    return validators_data;
}

/*
export async function query_supply(client: StakingClient) {
    let data = await client.staking.validators("BOND_STATUS_BONDED");

    let data2 = await client.bank.supplyOf("uatom");
}
*/

export async function connect_stargate_client(network_settings: NetworkSettings): Promise<boolean> {
    if (window.keplr) {
        await window.keplr.enable(network_settings.chain_id);
        const offlineSigner = window.keplr.getOfflineSigner(network_settings.chain_id);


        // You can get the address/public keys by `getAccounts` method.
        // It can return the array of address/public key.
        // But, currently, Keplr extension manages only one address/public key pair.
        // XXX: This line is needed to set the sender address for SigningCosmosClient.
        const accounts = await offlineSigner.getAccounts();

        // Initialize the gaia api with the offline signer that is injected by Keplr extension.
        /*
        const cosmJS = new SigningCosmosClient(
            'https://lcd-cosmoshub.keplr.app',
            accounts[0].address,
            offlineSigner
        );
        */
        
        const sign_client = await SigningStargateClient.connectWithSigner(network_settings.rpc, offlineSigner, {
            "gasPrice": GasPrice.fromString(
                `${network_settings.fees.fixed_min_gas_price}${network_settings.fees.denom}`
            )
        });

        READ_CLIENT.set(await create_client(network_settings.rpc));
        USER_ADDRESS.set(accounts[0].address);
        STARGATE_SIGNING_CLIENT.set(sign_client);

        return true;
    } else {
        return false;
    }

}

/*
export async function connect_keplr(network_settings: NetworkSettings): Promise<[Keplr, SigningStargateClient, string] | null> {
    if (window.keplr) {
        // Enabling before using the Keplr is recommended.
        // This method will ask the user whether to allow access if they haven't visited this website.
        // Also, it will request that the user unlock the wallet if the wallet is locked.
        await window.keplr.enable(network_settings.chain_id);
        const offlineSigner = window.keplr.getOfflineSigner(network_settings.chain_id);

        // You can get the address/public keys by `getAccounts` method.
        // It can return the array of address/public key.
        // But, currently, Keplr extension manages only one address/public key pair.
        // XXX: This line is needed to set the sender address for SigningCosmosClient.
        const accounts = await offlineSigner.getAccounts();

        // Initialize the gaia api with the offline signer that is injected by Keplr extension.
        const cosmJS = new SigningCosmosClient(
            'https://lcd-cosmoshub.keplr.app',
            accounts[0].address,
            offlineSigner
        );
        
        
        const sign_client = await SigningStargateClient.connectWithSigner(network_settings.rpc, offlineSigner);

        return [window.keplr, sign_client, accounts[0].address];
    } else {
        return null;
    }
}
*/



/*
export async function execute_staking(staking_targets: StakingTarget[], signing_client: SigningStargateClient, network_settings: NetworkSettings) {
    
    if (USER_ADDRESS) {
        const userAddress: string = $USER_ADDRESS;

    }
    const toStake: { validator: string; amount: Coin }[] = [];

    const stakingMessages = toStake
        .map((t) =>
            MsgDelegate.fromPartial({
                amount: t.amount,
                delegatorAddress: $USER_ADDRESS,
                validatorAddress: t.validator,
            })
        )
        .map((m) => ({
            typeUrl: "/cosmos.staking.v1beta1.MsgDelegate",
            value: m,
        }));

    const stakingTx = signing_client.signAndBroadcast(userAddress, stakingMessages, 'auto', HACKATHON_MEMO);

    toast.promise(stakingTx, {
        loading: "Sending Transaction...",
        success: (val) => {
            return `Success!\n Hash: ${val.transactionHash}`;
        },
        error: (err) => {
            return `Something went wrong.\n ${(err as Error).message}`;
        },
    });

    stakingTx.then() // et là tu refresh tes données
}
*/