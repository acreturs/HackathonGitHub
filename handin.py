from optibook.synchronous_client import Exchange
import time
import logging
import random
import math
from colorama import init, Fore, Back, Style



def get_price_per_share(id, volumeTotal):
    werte = exchange.get_last_price_book(id)
    # print(werte)
    bids = werte.bids
    asks = werte.asks
    index = 0
    stocksCount = 0
    ppbs = 0
    while index < len(bids):
        if (bids[index].volume >= volumeTotal and stocksCount == 0):
            ppbs = bids[index].price
    break
    elif (stocksCount > 0):
    rem = volumeTotal - stocksCount
    if (bids[index].volume >= rem):
        ppbs += rem * bids[index].price
    ppbs /= volumeTotal
    break
    if (bids[index].volume < rem):
        ppbs += bids[index].volume * bids[index].price
    stocksCount += bids[index].volume
    index += 1
    elif (bids[index].volume < volumeTotal):
    ppbs += bids[index].volume * bids[index].price
    stocksCount += bids[index].volume
    index += 1
    index2 = 0
    stocksCount2 = 0
    ppas = 0
    while index2 < len(asks):
        if (asks[index2].volume >= volumeTotal and stocksCount2 == 0):
            ppas = asks[index2].price
    break
    elif (stocksCount2 > 0):
    rem2 = volumeTotal - stocksCount2
    if (asks[index2].volume >= rem2):
        ppas += rem2 * asks[index2].price
    ppas /= volumeTotal
    break
    if (asks[index2].volume < rem2):
        ppas += asks[index2].volume * asks[index2].price
    stocksCount2 += asks[index2].volume
    index2 += 1
    elif (asks[index2].volume < volumeTotal):
    ppas += asks[index2].volume * asks[index2].price
    stocksCount2 += asks[index2].volume
    index2 += 1
    # print("start pps")
    # print(ppbs)
    # print(ppas)
    pps = (ppbs + ppas) / 2
    # print(pps)
    arr = [pps, ppbs, ppas]
    return arr


def get_ask_bid(id):
    bid_max = 0
    ask_min = 10000000
    werte = exchange.get_last_price_book(id)
    bid = werte.bids
    ask = werte.asks
    try:
        bid_max = bid[0].price
    ask_min = ask[0].price
    except:
    # print("no trade could be made")
    a = 0

    if (ask_min == 10000000):
        spread = 0
    ask_min = 0
    bid_max = 0
    arr = [bid_max, ask_min, spread]
    return arr

    spread = round(ask_min / bid_max - 1, 6)
    arr = [bid_max, ask_min, spread]
    return arr


def verifyTrade(id, volume, aorb, price):
    positions = exchange.get_positions()
    result = positions[id]

    # check that no position is above 500 in volume
    res = 0
    if (aorb == 'ask'):
        res = result - volume
    else:
        res = result + volume

    if (abs(res) > 500):
    # print("More thean 500 entities of this asset")
    # print(res)
    return 0;

    # check that there is no trade being made against us selves
    arr = exchange.get_outstanding_orders(id)

    # find the lowest asking price and the highest biding price
    low_ask = 10000000
    high_bid = 0
    for key, order in arr.items():
    # print("outstanding: ", order.instrument_id, order.price, order.side)
    if order.side == 'ask':
        if order.price < low_ask:
            low_ask = order.price
    else:
        if order.price > high_bid:
            high_bid = order.price

    # print("low_ask ", low_ask, " high_bid ", high_bid, id)
    if aorb == 'ask':
        if price <= high_bid:
    # print("Cancel because of trade with ourselves")
    return 0;

    if aorb == 'bid':
        if price >= low_ask:
    # print("Cancel because of trade with ourselves")
    return 0;

    # has to be improved

    # check if there is an outstanding order for this instrument
    arr3 = exchange.get_outstanding_orders(id)
    sum_bid = 0
    sum_ask = 0

    for order in arr.values():
        if order.side == 'ask':
            sum_ask += order.volume
    else:
        sum_bid += order.volume

    positions = exchange.get_positions()
    if (aorb == 'ask'):
        if (id == 'C1_FOSSIL_FUEL_ETF'):
            if ((positions[id] - volume) * 0.5 + positions['C1_GAS_INC'] >= -100 + sum_ask and (positions[id] -
                                                                                                volume) * 0.5 +
                    positions['C1_OIL_CORP'] >= -100 + sum_ask):
            return volume
    else:
    # print("Cancel: bucket stock relation")
    return 0
    if (id == 'C1_GAS_INC' or id == 'C1_OIL_CORP'):
        if ((positions[id] - volume) + 0.5 * positions['C1_FOSSIL_FUEL_ETF'] >= -100 + sum_ask):
            return volume
    else:
    # print("Cancel: bucket stock relation")
    return 0
    if (id == 'C2_GREEN_ENERGY_ETF'):
        if ((positions[id] - volume) * 0.5 + positions['C2_SOLAR_CO'] >= -100 + sum_ask and (positions[id] -
                                                                                             volume) * 0.5 + positions[
            'C2_WIND_LTD'] >= -100 + sum_ask):
            return volume
    else:
    # print("Cancel: bucket stock relation")
    return 0
    if (id == 'C2_SOLAR_CO' or id == 'C2_WIND_LTD'):
        if ((positions[id] - volume) + 0.5 * positions['C2_GREEN_ENERGY_ETF'] >= -100 + sum_ask):
            return volume
    else:
    # print("Cancel: bucket stock relation")
    return 0

    if (aorb == 'bid'):
        if (id == 'C1_FOSSIL_FUEL_ETF'):
            if ((positions[id] + volume) * 0.5 + positions['C1_GAS_INC'] <= 100 - sum_bid and
                    (positions[id] + volume) * 0.5 + positions['C1_OIL_CORP'] <= 100 - sum_bid):
            return volume
    else:
    # print("Cancel: bucket stock relation")
    return 0
    if (id == 'C1_GAS_INC' or id == 'C1_OIL_CORP'):
        if ((positions[id] + volume) + 0.5 * positions['C1_FOSSIL_FUEL_ETF'] <= 100 - sum_bid):
            return volume
    else:
    # print("Cancel: bucket stock relation")
    return 0
    if (id == 'C2_GREEN_ENERGY_ETF'):
        if ((positions[id] + volume) * 0.5 + positions['C2_SOLAR_CO'] <= 100 - sum_bid and
                (positions[id] + volume) * 0.5 + positions['C2_WIND_LTD'] <= 100 - sum_bid):
            return volume
    else:
    # print("Cancel: bucket stock relation")
    return 0
    if (id == 'C2_SOLAR_CO' or id == 'C2_WIND_LTD'):
        if ((positions[id] + volume) + 0.5 * positions['C2_GREEN_ENERGY_ETF'] <= 100 - sum_bid):
            return volume
    else:
    # print("Cancel: bucket stock relation")
    return 0


def addBidandAsk(id, volume):
    # avg = get_spread_avg(id)
    # print("avg")
    # print(avg)
    arr2 = get_price_per_share(id, volume)
    pps = arr2[0]
    ppbs = arr2[1]
    ppas = arr2[2]
    # print("pps and ppbs and ppas")
    # print(pps)
    # print(ppbs)
    # print(ppas)
    arr = get_ask_bid(id)
    # print("bid and ask and spread")
    # print(arr[0])
    # print(arr[1])
    # print(arr[2])
    # case 1: spread is in the middle
    # if pps > arr[0] + arr[2] * 0.4 and pps < arr[1] - arr[2] * 0.4:
    # print("liegt in der mitte")
    # ask_price = ppas - (ppas-ppbs) * 0.1
    # bid_price = ppbs + (ppas-ppbs) * 0.1
    ask_price = arr[1] - arr[2] * 0.3
    bid_price = arr[0] + arr[2] * 0.3
    # volume = 100
    # print("Profit")
    # print(exchange.get_pnl())
    temp1 = verifyTrade(id, volume, 'bid', bid_price)
    temp2 = verifyTrade(id, volume, 'ask', ask_price)
    possible_profit = ask_price - bid_price
    resp1 = False
    resp2 = False
    try:
        if (temp1 > 0 and temp2 > 0 and ask_price > 0 and bid_price > 0):
            resp1 = exchange.insert_order(id, price=bid_price, volume=temp1, side='bid',
                                          order_type='limit')
    # print("try trade: ", id, ask_price, 'ask')
    if (temp2 > 0 and ask_price > 0 and bid_price > 0):
        resp2 = exchange.insert_order(id, price=ask_price, volume=temp2, side='ask',
                                      order_type='limit')
    # print("try trade: ", id, bid_price, 'bid')

    else:
    # print("trade ask was cancelled because of verified")
    a = 2
    except:
    # print("error occurred maybe self trade")
    a = 3

    # print("the trade worked: ", possible_profit)
    # print("possible profit", possible_profit)
    # werte = exchange.get_last_price_book(id)
    # print(werte)
    # print("Profit")
    # print(exchange.get_pnl())
    # print("positions")
    # print(exchange.get_positions())

    check_outstanding(id)


def check_outstanding(id):
    arr = exchange.get_outstanding_orders(id)
    sum = 0

    for order in arr.values():
        sum += order.volume

    if sum > 200:
    # print("over 200 outstanding orders")
    # check how far the price of each order is from the ppc
    arr2 = get_price_per_share(id, 10)
    pps = arr2[0]

    for key, order in arr.items():
        diff = abs(order.price / pps - 1)
    arr3 = get_ask_bid(id)
    max_bid = arr3[0] + 0.25 * arr3[2]
    min_ask = arr3[1] - 0.25 * arr3[2]
    if diff > 0.02 or order.price > min_ask or order.price < max_bid:
        exchange.delete_order(id, order_id=key)
    # print("order deleted because too far from pps")
    time.sleep(0.07)
    sum -= order.volume

    # check that the sum is below 200
    if sum > 200:
        for key, order in arr.items():
            exchange.delete_order(id, order_id=key)
    sum -= order.volume
    # print("order deleted because too many orders")
    # print(order.volume)
    time.sleep(0.07)
    if (sum < 200):
        break


def delete_all_orders():
    assets = [['C2_WIND_LTD', 10], ['C2_SOLAR_CO', 10], ['C2_GREEN_ENERGY_ETF', 20],
              ['C1_FOSSIL_FUEL_ETF', 20], ['C1_OIL_CORP', 10], ['C1_GAS_INC', 10]]
    for i in range(0, 6):
        exchange.delete_orders(assets[i][0])


def overflowHandler():
    instruments = exchange.get_instruments()

    for instrument_id in instruments:
    # print("Preise von: ",instrument_id)
    werte = exchange.get_last_price_book(instrument_id)
    # print(werte)
    dic = exchange.get_positions()
    # print("Positionen in der id: ",dic[instrument_id])
    values = getLowestAskPrice(instrument_id)
    try:
        if dic[instrument_id] > 0:
            exchange.insert_order(instrument_id, price=values - 0.3, volume=dic[instrument_id],
                                  side='ask', order_type='limit')
    if dic[instrument_id] < 0:
        exchange.insert_order(instrument_id, price=values + 0.3, volume=abs(dic[instrument_id]),
                              side='bid', order_type='limit')
    except:
    # print("error")
    a = 4


def getLowestAskPrice(instrument_id):
    priceBook = exchange.get_last_price_book(instrument_id)
    if (len(priceBook.asks) > 0):
        return priceBook.asks[0].price
    else:
        return -1


def getHighestBidPrice(instrument_id):
    priceBook = exchange.get_last_price_book(instrument_id)
    if (len(priceBook.bids) > 0):
        return priceBook.bids[0].price
    else:
        return -1


def getLowestAskVolume(instrument_id):
    priceBook = exchange.get_last_price_book(instrument_id)
    if (len(priceBook.asks) > 0):
        return priceBook.asks[0].volume
    else:
        return -1


def getHighestBidVolume(instrument_id):
    priceBook = exchange.get_last_price_book(instrument_id)
    if (len(priceBook.bids) > 0):
        return priceBook.bids[0].volume
    else:
        return -1


def check_to_sell():
    # print("try to sell the positions")

    # this method should check whether or not to sell stocks
    # that are currently our positions
    assets = [['C2_WIND_LTD', 10], ['C2_SOLAR_CO', 10], ['C2_GREEN_ENERGY_ETF', 20],
              ['C1_FOSSIL_FUEL_ETF', 20], ['C1_OIL_CORP', 10], ['C1_GAS_INC', 10]]
    trade_history = exchange.get_trade_history(instrument_id)
    position = exchange.get_positions()
    # print("positions", position)

    for asset, vol in assets:
        avg_price = 0
    res = 0

    if position[asset] == 0:
    # can skip this position => position == 0
    continue

    # check whether position is pos or neg
    # aorb = ''
    if position[asset] > 0:
        aorb = 'bid'
    else:
        arob = 'ask'

    for trade in trade_history:
        if trade.instrument_id == asset and trade.aggressor_side == aorb:
            res += trade.volume
    avg_price += trade.volume * trade.price
    if res >= position[asset]:
    # reached the avg price
    avg_price = float(avg_price / res)
    break

    # check if we should sell
    pps = get_price_per_share(asset, vol)
    if aorb == 'bid' and avg_price > float(pps) * float(1.02):
        print("try to sell", asset)
    # man sollte verkaufen
    temp1 = verifyTrade(assset, vol, 'ask', avg_price)
    try:
        if (temp1 > 0):
            exchange.insert_order(asset, price=avg_price, volume=temp1, side='ask',
                                  order_type='limit')
    print("try sell ", asset, avg_price, 'ask')
    else:
    print("trade ask was cancelled because of verified")
    except:
    print("error occurred maybe self trade")

    if aorb == 'ask' and avg_price < float(pps) * float(0.98):
        print("try to buy", asset)
    # man sollte verkaufen
    temp1 = verifyTrade(assset, position[asset], 'bid', avg_price)
    try:
        if (temp1 > 0):
            exchange.insert_order(asset, price=avg_price, volume=temp1, side='bid',
                                  order_type='limit')
    print("try buy ", asset, avg_price, 'bid')
    else:
    print("trade ask was cancelled because of verified")
    except:
    print("error occurred maybe self trade")


def mainMeth():
    print("start profit")
    print(exchange.get_pnl())
    for l in range(0, 1):
        for j in range(0, 2):
            for i in range(0, 6):
            time.sleep(0.08)
    assets = [['C2_WIND_LTD', 10], ['C2_SOLAR_CO', 10], ['C2_GREEN_ENERGY_ETF', 20],
              ['C1_FOSSIL_FUEL_ETF', 20], ['C1_OIL_CORP', 10], ['C1_GAS_INC', 10]]
    addBidandAsk(assets[i][0], assets[i][1])

    print(exchange.get_positions())
    print("pnl ", exchange.get_pnl())

    werte = exchange.get_last_price_book(assets[i][0])
    print(werte)

    trade_history = exchange.poll_new_trades(assets[i][0])
    print("trades ", trade_history)

    outstanding = exchange.get_outstanding_orders(assets[i][0])
    print("outstanding ", outstanding)

    check_to_sell()
    overflowHandler()
    print("end profit")
    print(exchange.get_pnl())


def fossileBaskets():
    global counter
    global failedTrades
    id_gas = "C1_GAS_INC"
    id_oil = "C1_OIL_CORP"
    id_fossileETF = "C1_FOSSIL_FUEL_ETF"

    price_LowestAsk_Oil = getLowestAskPrice(id_oil)  # können dazu am billisgern einkaufen
    price_HighestBid_Oil = getHighestBidPrice(id_oil)  # teurste verkaufen

    price_LowestAsk_Gas = getLowestAskPrice(id_gas)  # ebenfalls billigste einkaufen
    price_HighestBid_Gas = getHighestBidPrice(id_gas)  # teuerste verkaufen

    price_LowestAsk_FossileETF = getLowestAskPrice(id_fossileETF)  # niedrigste preis um bastek zu


kaufen
price_HighestBid_FossileETF = getHighestBidPrice(id_fossileETF)  # teuerste verkaufen

price_min = min(price_LowestAsk_Oil, price_HighestBid_Oil, price_LowestAsk_Gas,
                price_HighestBid_Gas, price_LowestAsk_FossileETF, price_HighestBid_FossileETF)

price_BuyBothSingleStocks = (0.5 * price_LowestAsk_Oil + 0.5 * price_LowestAsk_Gas)
price_SellBothSingleStocks = (0.5 * price_HighestBid_Oil + 0.5 * price_HighestBid_Gas)

dif_SellBasketBuySingles = price_HighestBid_FossileETF - price_BuyBothSingleStocks
dif_BuyBasketSellSingles = price_LowestAsk_FossileETF - price_SellBothSingleStocks

failedTrades += 1

if dif_SellBasketBuySingles > 0.0:
# Buy single Stocks
# Sell basket
orderVolume = min(getLowestAskVolume(id_oil), getLowestAskVolume(id_gas),
                  getHighestBidVolume(id_fossileETF))

if orderVolume > 200:
    orderVolume = 200

if orderVolume > 0 and price_min > 0:
    exchange.insert_order(id_oil, price=price_LowestAsk_Oil, volume=orderVolume, side='bid',
                          order_type='limit')
exchange.insert_order(id_gas, price=price_LowestAsk_Gas, volume=orderVolume, side='bid',
                      order_type='limit')
exchange.insert_order(id_fossileETF, price=price_HighestBid_FossileETF,
                      volume=orderVolume, side='ask', order_type='limit')
overflowHandler()
counter += 1
failedTrades = 0

elif dif_BuyBasketSellSingles < 0.0:
# Buy Basket
# Sell single stock
orderVolume = min(getLowestAskVolume(id_fossileETF), getHighestBidVolume(id_oil),
                  getHighestBidVolume(id_gas))

if orderVolume > 200:
    orderVolume = 200

if orderVolume > 0 and price_min > 0:
    exchange.insert_order(id_fossileETF, price=price_LowestAsk_FossileETF,
                          volume=orderVolume, side='bid', order_type='limit')
exchange.insert_order(id_oil, price=price_HighestBid_Oil, volume=orderVolume, side='ask',
                      order_type='limit')
exchange.insert_order(id_gas, price=price_HighestBid_Gas, volume=orderVolume, side='ask',
                      order_type='limit')
counter += 1
failedTrades = 0


def greenBaskets():
    global counter
    global failedTrades
    id_solar = "C2_SOLAR_CO"  # "C1_OIL_CORP"
    id_wind = "C2_WIND_LTD"  # C1_GAS_INC"
    id_greenETF = "C2_GREEN_ENERGY_ETF"

    price_LowestAsk_Solar = getLowestAskPrice(id_solar)  # können dazu am billisgern einkaufen
    price_HighestBid_Solar = getHighestBidPrice(id_solar)  # teurste verkaufen

    price_LowestAsk_Wind = getLowestAskPrice(id_wind)  # ebenfalls billigste einkaufen
    price_HighestBid_Wind = getHighestBidPrice(id_wind)  # teuerste verkaufen

    price_LowestAsk_GreenETF = getLowestAskPrice(id_greenETF)  # niedrigste preis um bastek zu



    price_HighestBid_GreenETF = getHighestBidPrice(id_greenETF)  # teuerste verkaufen

    price_min = min(price_LowestAsk_Solar, price_HighestBid_Solar, price_LowestAsk_Wind,
                    price_HighestBid_Wind, price_LowestAsk_GreenETF, price_HighestBid_GreenETF)

    price_BuyBothSingleStocks = (0.5 * price_LowestAsk_Solar + 0.5 * price_LowestAsk_Wind)
    price_SellBothSingleStocks = (0.5 * price_HighestBid_Solar + 0.5 * price_HighestBid_Wind)

    failedTrades += 1

    dif_SellBasketBuySingles = price_HighestBid_GreenETF - price_BuyBothSingleStocks
    dif_BuyBasketSellSingles = price_LowestAsk_GreenETF - price_SellBothSingleStocks

if dif_SellBasketBuySingles > 0.0:
# Buy single Stocks
# Sell basket
    orderVolume = min(getLowestAskVolume(id_solar), getLowestAskVolume(id_wind),
                      getHighestBidVolume(id_greenETF))

if orderVolume > 200:
    orderVolume = 200

if orderVolume > 0 and price_min > 0:
        exchange.insert_order(id_solar, price=price_LowestAsk_Solar + 0.0, volume=orderVolume,
                              side='bid', order_type='limit')
    exchange.insert_order(id_wind, price=price_LowestAsk_Wind + 0.0, volume=orderVolume,
                          side='bid', order_type='limit')
    exchange.insert_order(id_greenETF, price=price_HighestBid_GreenETF - 0.0,
                          volume=orderVolume, side='ask', order_type='limit')
counter += 1
failedTrades = 0

elif dif_BuyBasketSellSingles < 0.0:
# Buy Basket
# Sell single stock
    orderVolume = min(getLowestAskVolume(id_greenETF), getHighestBidVolume(id_solar),
                      getHighestBidVolume(id_wind))

if orderVolume > 200:
    orderVolume = 200

if orderVolume > 0 and price_min > 0:
        exchange.insert_order(id_greenETF, price=price_LowestAsk_GreenETF + 0.0,
                              volume=orderVolume, side='bid', order_type='limit')
        exchange.insert_order(id_solar, price=price_HighestBid_Solar - 0.0, volume=orderVolume,
                              side='ask', order_type='limit')
        exchange.insert_order(id_wind, price=price_HighestBid_Wind - 0.0, volume=orderVolume,
                              side='ask', order_type='limit')
        counter += 1
        failedTrades = 0

init(autoreset=True)
if __name__ == "__main__":
    counter = 0
    failedTrades = 0
    print("hello world")
    logger = logging.getLogger('client')
    logger.setLevel('ERROR')
    print("Setup was successful.")
    exchange = Exchange()
    connected = exchange.connect()
    instruments = exchange.get_instruments()

    counter2 = 0

    while (True):

    try:

        # while(failedTrades < 200):
        time.sleep(0.01)
        greenBaskets()
        fossileBaskets()

    """ 
    for j in range(0,3):
    for i in range(0, 6):
    time.sleep(0.08)
    assets = [['C2_WIND_LTD', 10], ['C2_SOLAR_CO', 10], ['C2_GREEN_ENERGY_ETF', 20], 
    ['C1_FOSSIL_FUEL_ETF', 20], ['C1_OIL_CORP', 10], ['C1_GAS_INC', 10]]
    addBidandAsk(assets[i][0], assets[i][1])
   
    failedTrades = 0
    """

    except:
        exchange = Exchange()
        connected = exchange.connect()
        instruments = exchange.get_instruments()

        counter2 += 1
        if counter2 % 25 == 0:
            delete_all_orders()
        overflowHandler()

