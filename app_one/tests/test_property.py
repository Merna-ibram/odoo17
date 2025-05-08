from odoo.tests.common import TransactionCase
from odoo import fields

class TestProperty(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestProperty, self).setUp()

        # إنشاء سجل خاص بـ property
        self.property_01_rec = self.env['property'].create({
            'name': 'property 1000',
            'description': 'property 1000 description',
            'postcode': '1010',
            'date_availability': fields.Date.today(),
            'expected_price': 52000,
            'selling_price': 48000,
            'bedrooms': 5,
            'living_area': 120,
        })

    def test_01_property_values(self):
        property_id = self.property_01_rec


        self.assertRecordValues(property_id, [{
            'name': 'property 1000',
            'description': 'property 1000 description',
            'postcode': '1010',
            'date_availability': fields.Date.today(),
            'expected_price': 52000,
            'selling_price': 48000,
            'bedrooms': 5,
            'living_area': 120,
            'active': True,  # التأكد من أن الحقل 'active' مفعّل بشكل صحيح
        }])

        print(self.property_01_rec.read())

