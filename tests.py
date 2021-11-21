from app import create_app
from extensions import db
import unittest


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        with self.app.app_context():
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # POST: Создать нового пациента
    def test_create_new_patient(self):
        response = self.client.post(
            "/api/v1/patients",
            json={
                "name": "Afzal Asatov",
                "phone": "974544884",
                "birthday": "2000-03-07"
            }
        )
        self.assertIn("location", response.headers)
        self.assertIn("/api/v1/patients/", response.headers["Location"])
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        self.assertIn("/api/v1/patients/", response.json["location"])

    # POST: Создать нового пациента с неверными параметрами
    def test_create_new_patient_with_wrong_param(self):
        response = self.client.post(
            "/api/v1/patients",
            json={
                "names": "Afzal Asatov",
                "phone": "974544884",
                "birthday": "2000-03-07"
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json.keys())

    # GET: Получить список пациентов
    def test_get_all_patients(self):
        response = self.client.get("/api/v1/patients")
        self.assertEqual(response.status_code, 200)
        self.assertIn("patients", response.json.keys())

    # GET: Получить одного пациента
    def tests_get_one_patient_info(self):
        response = self.client.post(
            "/api/v1/patients",
            json={
                "name": "Afzal Asatov",
                "phone": "974544884",
                "birthday": "2000-03-07"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]

        response = self.client.get("/api/v1/patients/{}".format(uuid))
        self.assertEqual(response.status_code, 200)

    # GET: Получить информацию об одном не существующем пациенте
    def test_get_one_patient_empty_info(self):
        response = self.client.get(
            "/api/v1/patients/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)

    # DELETE: Удалить пациента по uuid
    def test_delete_patient(self):
        response = self.client.post(
            "/api/v1/patients",
            json={
                "name": "Afzal Asatov",
                "phone": "974544884",
                "birthday": "2000-03-07"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        response = self.client.delete("/api/v1/patients/{}".format(uuid))
        self.assertEqual(response.status_code, 200)

    # DELETE: Удалить пациента по несуществующему uuid
    def test_delete_empty_patient(self):
        response = self.client.delete(
            "/api/v1/patients/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)

    # PATCH: Обновить инормацию о пациенте
    def test_update_patient_info(self):
        response = self.client.post(
            "/api/v1/patients",
            json={
                "name": "Afzal Asatov",
                "phone": "974544884",
                "birthday": "2000-03-07"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        response = self.client.patch(
            "/api/v1/patients/{}".format(uuid),
            json={
                "name": "Tursunov Jasur"
            }
        )
        self.assertEqual(response.status_code, 200)

    # PATCH: Обновить пациента по несуществующему uuid
    def test_update_empty_patient(self):
        response = self.client.patch(
            "/api/v1/patients/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)

    # POST: Создать запись у врача
    def test_create_record(self):
        response = self.client.post(
            "/api/v1/patients",
            json={
                "name": "Afzal Asatov",
                "phone": "974544884",
                "birthday": "2000-03-07"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        response = self.client.post(
            "/api/v1/patients/{}".format(uuid),
            json={
                "doctor_uuid": "20e02bdd-273e-6u40-5ced-4a9637acb1f6",
                "date": "2021-01-01 00:00:00.000000",
                "used_services": "[1, 2, 3]",
                "disease": "Больной на голову",
                "discharge": "Увы. Ничего поделать нельзя",
                "payment_status": "False",
                "sum": "100000"
            }
        )
        self.assertEqual(response.status_code, 201)

    # POST: Создать запись по несуществующему uuid
    def tests_create_record_with_empty_uuid(self):
        response = self.client.post(
            "/api/v1/patients/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)

    # POST: Создать новую запись с неверными параметрами
    def test_create_new_record_with_wrong_param(self):
        response = self.client.post(
            "/api/v1/patients",
            json={
                "name": "Afzal Asatov",
                "phone": "974544884",
                "birthday": "2000-03-07"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        response = self.client.post(
            "/api/v1/patients/{}".format(uuid),
            json={
                "doctor_uuid": "20e02bdd-273e-6u40-5ced-4a9637acb1f6",
                "date": "2021-01-01 00:00:00.000000"
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json.keys())

    #------------------------------------------------------------------------

    # POST: Создать нового врача
    def test_create_new_doctor(self):
        response = self.client.post(
            "/api/v1/doctors",
            json={
                "name": "Qasimov Umid",
                "speciality": "Genikolog",
                "qualification": "Highest",
                "phone": "977745447"
            }
        )
        self.assertIn("location", response.headers)
        self.assertIn("/api/v1/doctors/", response.headers["Location"])
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        self.assertIn("/api/v1/doctors/", response.json["location"])

    # POST: Создать нового врача с неверными параметрами
    def test_create_new_doctor_with_wrong_param(self):
        response = self.client.post(
            "/api/v1/doctors",
            json={
                "names": "Afzal Asatov",
                "phone": "974544884",
                "birthday": "2000-03-07"
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json.keys())

    # GET: Получить список докторов
    def test_get_all_doctors(self):
        response = self.client.get("/api/v1/doctors")
        self.assertEqual(response.status_code, 200)
        self.assertIn("doctor", response.json.keys())

    # GET: Получить одного врача
    def tests_get_one_doctor_info(self):
        response = self.client.post(
            "/api/v1/doctors",
            json={
                "name": "Qasimov Umid",
                "speciality": "Genikolog",
                "qualification": "Highest",
                "phone": "977745447"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]

        response = self.client.get("/api/v1/doctors/{}".format(uuid))
        self.assertEqual(response.status_code, 200)

    # GET: Получить информацию об одном не существующем докторе
    def test_get_one_doctor_empty_info(self):
        response = self.client.get(
            "/api/v1/doctors/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)

    # DELETE: Удалить врача по uuid
    def test_delete_doctor(self):
        response = self.client.post(
            "/api/v1/doctors",
            json={
                "name": "Qasimov Umid",
                "speciality": "Genikolog",
                "qualification": "Highest",
                "phone": "977745447"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        response = self.client.delete("/api/v1/doctors/{}".format(uuid))
        self.assertEqual(response.status_code, 200)

        # DELETE: Удалить пациента по несуществующему uuid

    # GET: Удалить врача по несуществующему uuid
    def test_delete_empty_doctor(self):
        response = self.client.delete(
            "/api/v1/doctors/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)

    # PATCH: Обновить инормацию о враче
    def test_update_doctor_info(self):
        response = self.client.post(
            "/api/v1/doctors",
            json={
                "name": "Qasimov Umid",
                "speciality": "Genikolog",
                "qualification": "Highest",
                "phone": "977745447"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        response = self.client.patch(
            "/api/v1/doctors/{}".format(uuid),
            json={
                "name": "Tursunov Jasur"
            }
        )
        self.assertEqual(response.status_code, 200)

    # PATCH: Обновить врача по несуществующему uuid
    def test_update_empty_doctor(self):
        response = self.client.patch(
            "/api/v1/doctors/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)

    #------------------------------------------------------------------------

    # GET: Получить список записей
    def test_get_all_records(self):
        response = self.client.get("/api/v1/records")
        self.assertEqual(response.status_code, 200)
        self.assertIn("records", response.json.keys())

    # GET: Получить одну запись
    def tests_get_one_record_info(self):
        response = self.client.post(
            "/api/v1/patients",
            json={
                "name": "Afzal Asatov",
                "phone": "974544884",
                "birthday": "2000-03-07"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        response = self.client.post(
            "/api/v1/patients/{}".format(uuid),
            json={
                "doctor_uuid": "20e02bdd-273e-6u40-5ced-4a9637acb1f6",
                "date": "2021-01-01 00:00:00.000000",
                "used_services": "[1, 2, 3]",
                "disease": "Больной на голову",
                "discharge": "Увы. Ничего поделать нельзя",
                "payment_status": "False",
                "sum": "100000"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        response = self.client.get("/api/v1/records/{}".format(uuid))
        self.assertEqual(response.status_code, 200)

    # GET: Получить информацию об одной не существующей записи
    def test_get_one_record_empty_info(self):
        response = self.client.get(
            "/api/v1/records/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)

    # DELETE: Удалить запись по uuid
    def test_delete_record(self):
        response = self.client.post(
            "/api/v1/patients",
            json={
                "name": "Afzal Asatov",
                "phone": "974544884",
                "birthday": "2000-03-07"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        response = self.client.post(
            "/api/v1/patients/{}".format(uuid),
            json={
                "doctor_uuid": "20e02bdd-273e-6u40-5ced-4a9637acb1f6",
                "date": "2021-01-01 00:00:00.000000",
                "used_services": "[1, 2, 3]",
                "disease": "Больной на голову",
                "discharge": "Увы. Ничего поделать нельзя",
                "payment_status": "False",
                "sum": "100000"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        response = self.client.delete("/api/v1/records/{}".format(uuid))
        self.assertEqual(response.status_code, 200)

        # DELETE: Удалить пациента по несуществующему uuid

    # GET: Удалить запись по несуществующему uuid
    def test_delete_empty_record(self):
        response = self.client.delete(
            "/api/v1/records/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)

    # PATCH: Обновить инормацию о записе
    def test_update_record_info(self):
        response = self.client.post(
            "/api/v1/patients",
            json={
                "name": "Afzal Asatov",
                "phone": "974544884",
                "birthday": "2000-03-07"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        response = self.client.post(
            "/api/v1/patients/{}".format(uuid),
            json={
                "doctor_uuid": "20e02bdd-273e-6u40-5ced-4a9637acb1f6",
                "date": "2021-01-01 00:00:00.000000",
                "used_services": "[1, 2, 3]",
                "disease": "Больной на голову",
                "discharge": "Увы. Ничего поделать нельзя",
                "payment_status": "False",
                "sum": "100000"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("location", response.json.keys())
        uuid = response.json["location"].split("/")[-1]
        response = self.client.patch(
            "/api/v1/records/{}".format(uuid),
            json={
                "payment_status": 1
            }
        )
        self.assertEqual(response.status_code, 200)

    # PATCH: Обновить запись по несуществующему uuid
    def test_update_empty_record(self):
        response = self.client.patch(
            "/api/v1/records/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()