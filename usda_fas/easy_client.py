from typing import List, Dict, Any, Optional
from .api.esr import ESRClient
from .api.gats import GATSClient
from .api.psd import PSDClient

class USDAFASEasyClient(ESRClient, GATSClient, PSDClient):
    """
    High-level client that aggregates ESR, GATS, and PSD functionality.
    Provides 'easy query' methods to automatically join and normalize data.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        # Caches for reference data
        self._esr_countries_map = None # Maps countryCode -> full country record
        self._esr_regions_map = None   # Maps regionId -> regionName
        self._esr_commodities_map = None
        self._esr_units_map = None
        self._psd_countries_map = None
        self._psd_commodities_map = None
        self._psd_units_map = None
        self._psd_attributes_map = None

    def _ensure_esr_ref_data(self):
        """Lazy load ESR reference data."""
        if not self._esr_regions_map:
            regions = self.get_esr_regions()
            self._esr_regions_map = {str(r.get('regionId')): r.get('regionName') for r in regions}

        if not self._esr_countries_map:
            countries = self.get_esr_countries()
            # Cache the whole record so we can access description, genc, regionId
            self._esr_countries_map = {str(c.get('countryCode')): c for c in countries}
        
        if not self._esr_commodities_map:
            commodities = self.get_esr_commodities()
            self._esr_commodities_map = {str(c.get('commodityCode')): c.get('commodityName') for c in commodities}

        if not self._esr_units_map:
            units = self.get_esr_units_of_measure()
            self._esr_units_map = {str(u.get('unitId')): u.get('unitNames') for u in units}

    def _ensure_psd_ref_data(self):
        """Lazy load PSD reference data."""
        if not self._psd_countries_map:
            countries = self.get_psd_countries()
            self._psd_countries_map = {str(c.get('countryCode')): c.get('countryName') for c in countries}

        if not self._psd_commodities_map:
            commodities = self.get_psd_commodities()
            self._psd_commodities_map = {str(c.get('commodityCode')): c.get('commodityName') for c in commodities}
        
        if not self._psd_units_map:
            units = self.get_psd_units_of_measure()
            self._psd_units_map = {str(u.get('unitId')): u.get('unitDescription') for u in units}
        
        if not self._psd_attributes_map:
            attrs = self.get_psd_commodity_attributes()
            self._psd_attributes_map = {str(a.get('attributeId')): a.get('attributeName') for a in attrs}

    def get_esr_exports_normalized(self, commodity_code: int, market_year: int) -> List[Dict[str, Any]]:
        """
        Get ESR export data with Country and Commodity names instead of just codes.
        Now includes countryDescription, gencCode, and regionName.
        """
        self._ensure_esr_ref_data()
        data = self.get_esr_exports_all_countries(commodity_code, market_year)
        
        normalized_data = []
        for record in data:
            new_record = record.copy()
            # Enrich with names
            c_code = str(record.get('countryCode', ''))
            com_code = str(record.get('commodityCode', ''))
            unit_id = str(record.get('unitId', ''))
            
            if c_code in self._esr_countries_map:
                country_data = self._esr_countries_map[c_code]
                new_record['countryName'] = country_data.get('countryName')
                new_record['countryDescription'] = country_data.get('countryDescription')
                new_record['gencCode'] = country_data.get('gencCode')
                
                # Enrich Region Name using regionId from country data
                region_id = str(country_data.get('regionId', ''))
                if region_id in self._esr_regions_map:
                    new_record['regionName'] = self._esr_regions_map[region_id]
                else:
                    new_record['regionName'] = None

            if com_code in self._esr_commodities_map:
                new_record['commodityName'] = self._esr_commodities_map[com_code]
            if unit_id in self._esr_units_map:
                new_record['unitName'] = self._esr_units_map[unit_id]
                
            normalized_data.append(new_record)
            
        return normalized_data

    def get_psd_data_normalized(self, commodity_code: str, market_year: int) -> List[Dict[str, Any]]:
        """
        Get PSD data with Country, Commodity, Unit, and Attribute names.
        """
        self._ensure_psd_ref_data()
        data = self.get_psd_commodity_data_by_year(commodity_code, market_year)
        
        normalized_data = []
        for record in data:
            new_record = record.copy()
            c_code = str(record.get('countryCode', ''))
            com_code = str(record.get('commodityCode', ''))
            unit_id = str(record.get('unitId', ''))
            attr_id = str(record.get('attributeId', ''))
            
            if c_code in self._psd_countries_map:
                new_record['countryName'] = self._psd_countries_map[c_code]
            if com_code in self._psd_commodities_map:
                new_record['commodityName'] = self._psd_commodities_map[com_code]
            if unit_id in self._psd_units_map:
                new_record['unitName'] = self._psd_units_map[unit_id]
            if attr_id in self._psd_attributes_map:
                new_record['attributeName'] = self._psd_attributes_map[attr_id]
            
            normalized_data.append(new_record)
            
        return normalized_data
