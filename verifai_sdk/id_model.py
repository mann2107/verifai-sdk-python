

class IdModel:
    """
    We suggest to always use a VerifaiDocument whenever possible.

    Data model to represent the responses that come from the id-models
    api. It is quite limited. You can get a VerifaiDocument result
    object if you get the 'data' from this model and pass it along
    as 'request' data in VerifaiDocument init.
    """
    data = None

    uuid = None
    type = None
    model = None
    country = None
    width_mm = None
    height_mm = None
    sample_front = None
    has_mrz = None
    zones = []

    def __init__(self, id_model_respone=None):
        if id_model_respone:
            self.data = id_model_respone

            self.uuid = id_model_respone['uuid']
            self.type = id_model_respone['type']
            self.model = id_model_respone['model']
            self.country = id_model_respone['country']
            self.width_mm = id_model_respone['width_mm']
            self.height_mm = id_model_respone['height_mm']
            self.sample_front = id_model_respone['sample_front']
            self.has_mrz = bool(id_model_respone['has_mrz'])
            self.zones = id_model_respone['zones']
        else:
            self.data = None

            self.uuid = None
            self.type = None
            self.model = None
            self.country = None
            self.width_mm = None
            self.height_mm = None
            self.sample_front = None
            self.has_mrz = None
            self.zones = []
