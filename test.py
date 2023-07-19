import pandas as pd
from web3r import Web3R

#EXAMPLE - Finding a merge of swaps and transfers
if __name__ == '__main__':

    provider_url = ''
    etherscan_api_token = ''

    # Instantiate the web3 researc provider with etherscan and infura
    web3_provider = Web3R.HTTPProvider(provider_url)
    web3r = Web3R(web3_provider=web3_provider, etherscan_api_token=etherscan_api_token)

    #Exploring WETH Based Tokens
    WETH_ADDRESS = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'

    # Tokens used in the pricing 
    WETH_pools = web3r.grph_uniV3.get_all_pools_by_one_address(WETH_ADDRESS)

    # Selecting the first pool of the WETH pools
    graph_pool = WETH_pools[32]

    # Finding the information for token0
    token0 = web3r.tokens.get_token(graph_pool.token0_address)
    token1 = web3r.tokens.get_token(graph_pool.token1_address)

    # Getting all the pool initialisation variables
    v3_pool_address, v3_pool, v3_order_correct = web3r.pricer.get_v3_pool_info(token0, token1, graph_pool.fee_tier)

    #Getting all the swaps and transfers via the pool
    df_1 = pd.DataFrame(web3r.tokens.get_all_transfers(token0))
    df_2 = pd.DataFrame(web3r.pricer.get_all_v3_swaps_by_pool(v3_pool))

    df_merged = pd.merge(df_1, df_2, how='outer', on='transactionHash')
    print(df_merged)