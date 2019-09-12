def initializeTableDic(dicTable): #ERROR INFO Debug
    for dicName in dicTable.keys():
        dicTable[dicName] = ''

dicTable = {
    'KMIG_NV_CMPX' :
        {
            'NV_CMPX_ID': None,
            'NV_CMPX_NM': None,
            'GOV_LEGL_DONG_CD': None,
            'NV_CMPX_KND': None,
            'BAS_ADDR': None,
            'DTL_ADDR': None,
            'X_COOR_VAL': None,
            'Y_COOR_VAL': None,
            'TOT_HSHL_CNT': None,
            'TOT_DONG_CNT': None,
            'MAX_FLR': None,
            'MIN_FLR': None,
            'CMPL_YYMM': None,
            'SALE_CNT': None,
            'JS_CNT': None,
            'WS_CNT': None,
            'SHRT_RENT_CNT': None,
            'CMPX_CTGR': None,
            'BLD_CO_NM': None,
            'TOT_PARK_CNT': None,
            'HSHL_PER_PARK_CNT': None,
            'HEAT_WAY': None,
            'HEAT_FUEL': None,
            'FAR': None,
            'BTLR': None,
            'AREA_LST': None,
            'MGMT_CO_TEL': None,
            'SBWY_INFO': None,
            'WASP_PIPE_RPLC': None,
            'MIG_RSN': None,
            'REG_USER_ID': None,
            'REG_DTM': None,
            'CHG_USER_ID': None,
            'CHG_DTM': None
        }
    ,
    'KMIG_NV_CMPX_IMG' :
        {
            'NV_CMPX_ID': None,
            'IMG_CORS': None,
            'IMG_ID': None,
            'NEW_OLD_CL': None,
            'IMG_CTGR_NM': None,
            'IMG_DESC': None,
            'IMG_REG_DTM':None,
            'IMG_SORT': None,
            'REG_USER_ID': None,
            'REG_DTM': None,
            'CHG_USER_ID': None,
            'CHG_DTM': None
        }
}