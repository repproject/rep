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
            'buildingRegister':'CMPX_REG_VAL'
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
            'imageOrder': 'IMG_SORT'
        }
    ,
    'KMIG_NV_CMPX_RBLD':
        {
            'businessStep': 'BIZ_STEP',
            'selectedBuilder': 'CHC_BLD_CO',
            'householdCount': 'EXP_HSHL_CNT',
            'floorAreaRatio': 'EXP_FAR',
            'builderTelNo': 'GULD_TEL',
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
            'entranceType':'DOOR_STRC'
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
            'dealPricePerSpaceMin' : 'MSML_PYNG_PER_AMT',
            'dealPricePerSpaceMax' : 'MBIG_PYNG_PER_AMT',
            'dealPriceString' : 'AMT_STR',
            'dealPricePerSpaceString' : 'PYNG_PER_AMT_STR',
            'leasePriceString' : 'JS_PRC_STR',
            'leasePricePerSpaceString' : 'JS_PYNG_PER_PRC_STR',
            'leasePriceRateString' : 'JS_PRC_RATE_STR',
        }
}