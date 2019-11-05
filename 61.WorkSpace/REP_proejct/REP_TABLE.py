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
            'ROAD_NM_BAS_ADDR' : None,
            'ROAD_NM_DTL_ADDR' : None,
            'X_COOR_VAL': None,
            'Y_COOR_VAL': None,
            'TOT_HSHL_CNT': None,
            'TOT_RENT_HSHL_CNT': None,
            'TOT_DONG_CNT': None,
            'MAX_FLR': None,
            'MIN_FLR': None,
            'CMPL_YYMM': None,
            'SALE_CNT': None,
            'JS_CNT': None,
            'WS_CNT': None,
            'SHRT_RENT_CNT': 0,
            'BLD_CO_NM': None,
            'TOT_PARK_CNT': 0,
            'HSHL_PER_PARK_CNT': 0,
            'HEAT_WAY': None,
            'HEAT_FUEL': None,
            'FAR': None,
            'BTLR': None,
            'MBIG_SPLY_AREA' : None,
            'MSML_SPLY_AREA' : None,
            'CMPX_REG_VAL' : None,
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
    ,'KMIG_NV_CMPX_RBLD' :
        {
            'NV_CMPX_ID': None,
            'BIZ_STEP': None,
            'CHC_BLD_CO': None,
            'EXP_HSHL_CNT': None,
            'EXP_FAR': None,
            'GULD_TEL': None,
            'EXP_ASGN_AREA': None,
            'REG_USER_ID': None,
            'REG_DTM': None,
            'CHG_USER_ID': None,
            'CHG_DTM': None
        }
    ,'KMIG_NV_CMPX_TYP' :
        {
            'NV_CMPX_ID' : None,
            'NV_CMPX_TYP_SEQ' : None,
            'CMPX_TYP_NM' : None,
            'SPLY_AREA' : None,
            'ONLY_AREA' : None,
            'DOOR_STRC' : None,
            'ROOM_CNT' : None,
            'BATH_CNT' : None,
            'SOH_HSHL_CNT' : None,
            'IMG_URL' : None,
            'SPLY_AREA_NUM' : None,
            'ONLY_AREA_NUM' : None,
            'RET_TYP_CD' : None,
            'REG_USER_ID' : None,
            'REG_DTM' : None,
            'CHG_USER_ID' : None,
            'CHG_DTM' : None,

        }
    ,'KMIG_NV_CMPX_TYP_IMG' :
        {
            'NV_CMPX_ID' : None,
            'NV_CMPX_TYP_SEQ' : None,
            'IMG_ID' : None,
            'IMG_SORT' : None,
            'IMG_CORS' : None,
            'IMG_TYP_CD' : None,
            'REG_USER_ID' : None,
            'REG_DTM' : None,
            'CHG_USER_ID' : None,
            'CHG_DTM' : None,
        }
    ,'KMIG_NV_CMPX_TYP_STAT' :
        {
            'NV_CMPX_ID': None,
            'NV_CMPX_TYP_SEQ': None,
            'SALE_CNT': None,
            'JS_CNT': None,
            'WS_CNT': None,
            'SHRT_RENT_CNT': None,
            'MSML_PRC_AMT_STR': None,
            'MBIG_PRC_AMT_STR': None,
            'MSML_PYNG_PER_AMT': None,
            'MBIG_PYNG_PER_AMT': None,
            'AMT_STR': None,
            'PYNG_PER_AMT_STR': None,
            'JS_PRC_STR': None,
            'JS_PYNG_PER_PRC_STR': None,
            'JS_PRC_RATE_STR': None,
            'WS_PRC_STR': None,
            'WS_DPST_MSML_AMT_STR': None,
            'WS_MSML_PRC_STR': None,
            'WS_DPST_MBIG_AMT_STR': None,
            'WS_MBIG_PRC_STR': None,
            'REG_USER_ID': None,
            'REG_DTM': None,
            'CHG_USER_ID': None,
            'CHG_DTM': None,
        }
}