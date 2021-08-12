dicMigMapp = {
    'KMIG_NV_CMPX' :
        {
            'complexNo': 'NV_CMPX_ID',
            'complexName': 'NV_CMPX_NM',
            'cortarNo': 'GOV_LEGL_DONG_CD',
            'realEstateTypeCode': 'NV_CMPX_KND',
            'cortarAddress': 'BAS_ADDR',
            'detailAddress': 'DTL_ADDR',
            'roadAddressPrefix': 'ROAD_NM_BAS_ADDR',
            'roadAddress':'ROAD_NM_DTL_ADDR',
            'address' : 'ADDR',
            'latitude': 'X_COOR_VAL',
            'longitude': 'Y_COOR_VAL',
            'totalHouseholdCount': 'TOT_HSHL_CNT',
            'totalLeaseHouseholdCount': 'TOT_RENT_HSHL_CNT',
            'totalBuildingCount': 'TOT_DONG_CNT',
            'highFloor': 'MAX_FLR',
            'lowFloor': 'MIN_FLR',
            'completionYearMonth': 'CMPL_YYMM',
            'dealCount': 'SALE_CNT',
            'leaseCount': 'JS_CNT',
            'rentCount': 'WS_CNT',
            'shortTermRentCount': 'SHRT_RENT_CNT',
            'batlRatio':'FAR',
            'btlRatio':'BTLR',
            'maxSupplyArea':'MBIG_SPLY_AREA',
            'minSupplyArea':'MSML_SPLY_AREA',
            'parkingCountByHousehold':'HSHL_PER_PARK_CNT',
            'constructionCompanyName':'BLD_CO_NM',
            'heatMethodTypeCode':'HEAT_WAY',
            'heatFuelTypeCode':'HEAT_FUEL',
            'pyoengNames':'AREA_LST',
            'managementOfficeTelNo':'MGMT_CO_TEL',
            'buildingRegister':'CMPX_REG_VAL',
            'realEstateTypeName' : None,
            'totalDongCount': 'WHL_DONG_CNT',
            'isBookmarked':'BMAK_YN',
            'averageMaintenanceCost' : None,
            'articleStatistics' : None,
            'plumbReplace':'WASP_PIPE_RPLC'
        }
    ,
    'KMIG_NV_CMPX_IMG':
        {
            'imageSrc': 'IMG_CORS',
            'imageId': 'IMG_ID',
            'newOldGbn': 'NEW_OLD_CL',
            'smallCategoryName': 'IMG_CTGR_NM',
            'explaination': 'IMG_DESC',
            'registYmdt': 'IMG_REG_DTM',
            'imageOrder': 'IMG_SORT',
            'imageKey': 'IMG_KEY_SEQ',
            'imageType' : 'IMG_TYP_CD',
            'etcItem1' : 'ETC_ITEM_NM'
        }
    ,
    'KMIG_NV_CMPX_RBLD':
        {
            'businessStep': 'BIZ_STEP',
            'selectedBuilder': 'CHC_BLD_CO',
            'householdCount': 'EXP_HSHL_CNT',
            'floorAreaRatio': 'EXP_FAR',
            'builderTelNo': 'GULD_TEL',
            'assignedArea': 'EXP_ASGN_AREA_STR'
        }
    ,
    'KMIG_NV_CMPX_TYP':
        {
            'pyeongNo': 'NV_CMPX_TYP_SEQ',
            'supplyAreaDouble': 'SPLY_AREA_NUM',
            'supplyArea': 'SPLY_AREA',
            'pyeongName': 'CMPX_TYP_NM',
            'exclusiveArea': 'ONLY_AREA',
            'householdCountByPyeong': 'SOH_HSHL_CNT',
            'realEstateTypeCode':'RET_TYP_CD',
            'entranceType':'DOOR_STRC',
            'supplyPyeong': None,
            'pyeongName2': None,
            'exclusivePyeong': None,
            'exclusiveRate': None,
            'grandPlanList': None,
            'maintenanceCostList' : None,
            'landPriceMaxByPtp':None,
            'articleStatistics':None,
            'averageMaintenanceCost':None,
            'roomCnt':'ROOM_CNT_STR',
            'bathroomCnt':'BATH_CNT_STR',
            'dealRestrictionYearMonthDay':'DEAL_LMIT_YMD',
            'isalePriceByLetter':'DCNT_PRC_LTR_STR',
            'isalePrice':'DCNT_PRC_STR',
            'monopolyPossibleYmd' : 'DEAL_PSBL_YMD'
        }
    ,
    'KMIG_NV_CMPX_TYP_IMG':
        {
            'imageId': 'IMG_ID',
            'imageOrder': 'IMG_SORT',
            'imageSrc': 'IMG_CORS',
            'imageType': 'IMG_TYP_CD',
        }
    ,
    'KMIG_NV_CMPX_TYP_STAT':
        {
            'dealCount' : 'SALE_CNT',
            'leaseCount' : 'JS_CNT',
            'rentCount' : 'WS_CNT',
            'shortTermRentCount' : 'SHRT_RENT_CNT',
            'dealPriceMin' : 'MSML_PRC_AMT_STR',
            'dealPriceMax' : 'MBIG_PRC_AMT_STR',
            'dealPricePerSpaceMin' : 'MSML_PYNG_PER_AMT_STR',
            'dealPricePerSpaceMax' : 'MBIG_PYNG_PER_AMT_STR',
            'dealPriceString' : 'AMT_STR',
            'dealPricePerSpaceString' : 'PYNG_PER_AMT_STR',
            'leasePriceString' : 'JS_PRC_STR',
            'leasePricePerSpaceString' : 'JS_PYNG_PER_PRC_STR',
            'leasePriceRateString' : 'JS_PRC_RATE_STR',
            'leasePriceMin' : 'JS_PRC_MSML_AMT_STR',
            'leasePriceMax' : 'JS_PRC_MBIG_AMT_STR',
            'leasePricePerSpaceMin' : 'JS_PYNG_PER_MSML_PRC_STR',
            'leasePricePerSpaceMax' : 'JS_PYNG_PER_MBIG_PRC_STR',
            'leasePriceRateMin' : 'JS_PRC_MSML_PRC_STR',
            'leasePriceRateMax' : 'JS_PRC_RATE_MBIG_PRC_STR',
            'rentPriceString' : 'WS_PRC_STR',
            'rentDepositPriceMin' : 'WS_DPST_MSML_AMT_STR',
            'rentPriceMin' : 'WS_MSML_PRC_STR',
            'rentDepositPriceMax' : 'WS_DPST_MBIG_AMT_STR',
            'rentPriceMax' : 'WS_MBIG_PRC_STR',
            'pyeongNo' : None
        }
    ,
    'KMIG_BB_LV1_REGN':
        {
            'code' : 'BB_LV1_REGN_CD',
            'name' : 'BB_LV1_REGN_NM'
        }
    ,
    'KMIG_BB_CMPX_TYP_MON_PRC':
        {
            'sdate_ym': 'STD_YYMM',
            'sdate_ymd': 'STD_YMD',
            'prc_l': 'DOWN_PRC',
            'prc_h': 'UP_PRC',
            'change_prc': 'CHG_PRC',
            'rnt_l': 'DOWN_JS_PRC',
            'rnt_h': 'UP_JS_PRC',
            'change_rnt': 'CHG_JS_PRC',
        }
    ,
    'KMIG_NV_CMPX_ATCL':
        {
            'articleNo': 'ATCL_NUM',
            'articleName': 'NV_CMPX_NM',
            'realEstateTypeCode': 'NV_CMPX_KND',
            'realEstateTypeName': 'NV_CMPX_KND_NM',
            'articleRealEstateTypeCode': 'NV_ATCL_CMPX_TYP_CD',
            'area1': 'SPLY_AREA_STR',
            'area2': 'ONLY_AREA_STR',
            'tagList': None,
            'articleStatus': 'NV_ATCL_STAT_CD',
            'tradeTypeCode': 'NV_DEAL_TYP_CD',
            'tradeTypeName': 'NV_CMPX_NM',
            'verificationTypeCode': 'NV_VRFY_TYP_CD',
            'floorInfo': 'FLR_INFO',
            'priceChangeState': 'PRC_CHG_STAT_CD',
            'isPriceModification': 'PRC_CHG_YN',
            'dealOrWarrantPrc': 'DEAL_PRC_NM',
            'premiumPrc': 'PRMU_PRC_NM',
            'rentPrc': 'RENT_PRC_NM',
            'sameAddrPremiumMax': 'SAME_ADDR_PRMU_MBIG_PRC_NM',
            'sameAddrPremiumMin':'SAME_ADDR_PRMU_MSML_PRC_NM',
            'areaName': 'CMPX_TYP_NM',
            'direction': 'EXPS_NM',
            'articleConfirmYmd': 'ATCL_CHK_YMD',
            'tradeCompleteYmd': 'DEAL_CMPL_YMD',
            'articleFeatureDesc': 'ATCL_DESC',
            'buildingName': 'DONG_NM',
            'sameAddrCnt': 'SAME_ADDR_CNT',
            'sameAddrDirectCnt': 'SAME_ADDR_DRCT_CNT',
            'sameAddrMaxPrc': 'SAME_ADDR_MBIG_PRC_NM',
            'sameAddrMinPrc': 'SAME_ADDR_MSML_PRC_NM',
            'cpid': 'PRVD_CO_ID',
            'cpName': 'PRVD_CO_NM',
            'cpPcArticleUrl': 'PRVD_ATCL_ADDR',
            'cpPcArticleBridgeUrl': 'PRVD_ATCL_LINK_URL',
            'cpPcArticleLinkUseAtArticleTitleYn': 'PRVD_ATCL_LINK_TITL_USE_YN',
            'cpPcArticleLinkUseAtCpNameYn': 'PRVD_ATCL_LINK_USE_PRVD_CO_NM_YN',
            'cpMobileArticleUrl': 'PRVD_MBL_ATCL_URL',
            'cpMobileArticleLinkUseAtArticleTitleYn': 'PRVD_MBL_LINK_TITL_USE_YN',
            'cpMobileArticleLinkUseAtCpNameYn': 'PRVD_MBL_LINK_PRVD_CO_NM_USE_YN',
            'latitude': 'X_COOR_VAL',
            'longitude': 'Y_COOR_VAL',
            'isLocationShow': 'LOC_MARK_YN',
            'realtorName': 'LREA_NM',
            'realtorId': 'LREA_ID',
            'isDirectTrade': 'DRCT_DEAL_YN',
            'isInterest': None,
            'sellerPhoneNum': 'SELL_USER_CELL_NUM',
            'detailAddress': 'DTL_ADDR',
            'detailAddressYn': 'DTL_ADDR_YN',
            'tradeCheckedByOwner': 'OWNER_CHK_YN',
            'representativeImgUrl': 'RPSN_IMG_URL',
            'representativeImgTypeCode': 'RPSN_IMG_TYP_CD',
            'representativeImgThumb': 'RPSN_IMG_THMB_NM',
            'siteImageCount': 'IMG_CNT',
            'sellerName': 'SELL_USER_NM',
            'tradeYearMonth': 'REAL_DEAL_YYMM',
            'tradeDayClusterCode': 'REAL_DEAL_YMD_CLCT_CD',
            'tradeDayClusterName': 'REAL_DEAL_YMD_CLCT_NM',
            'tradeDealPrice': 'REAL_DEAL_PRC_NM',
            'tradeDepositPrice': 'REAL_DEAL_DPST_NM',
            'tradeRentPrice': 'REAL_DEAL_RENT_PRC_NM'
        }
    ,
    'KMIG_NV_CMPX_TYP_MNTN_PRC':
        {
            'basisYearMonth': 'STD_YYMM',
            'totalPrice': 'TOT_PRC_NM'
        }

}

if __name__ == '__main__':
    for col in dicMigMapp['KMIG_NV_CMPX_ATCL'].keys():
        print(col + "|" + str(dicMigMapp['KMIG_NV_CMPX_ATCL'][col]))