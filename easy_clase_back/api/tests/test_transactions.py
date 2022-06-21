from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Module, Reservation
from api.models import Transaction as TransactionModel


class Transaction(APITestCase):
    def test_create_transaction(self):
        self.student = get_user_model().objects.create_user(
            mail="student@uc.cl",
            password="pass1234test",
            first_name="student",
            last_name="student",
            phone="66783359",
            is_student=True)

        self.teacher = get_user_model().objects.create_user(
            mail="teacher@uc.cl",
            password="pass1234test",
            first_name="teacher",
            last_name="teacher",
            phone="66783309",
            is_teacher=True)

        self.token = RefreshToken.for_user(user=self.student).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        self.module = Module.objects.create(teacher=self.teacher, start_time="13:00:00",
                                            end_time="14:00:00", date="2023-05-05")
        self.reservation = Reservation.objects.create(student=self.student, module=self.module, teacher_done=True, student_done=True)
        post_data = {
            "reservation": self.reservation.id,
            "amount": 15000,
            "transaction_method": "paypal"
        }
        response = self.client.post(
            '/api/transaction/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_transaction_as_teacher(self):
        self.student = get_user_model().objects.create_user(
            mail="student@uc.cl",
            password="pass1234test",
            first_name="student",
            last_name="student",
            phone="66783359",
            is_student=True)

        self.teacher = get_user_model().objects.create_user(
            mail="teacher@uc.cl",
            password="pass1234test",
            first_name="teacher",
            last_name="teacher",
            phone="66783309",
            is_teacher=True)

        self.token = RefreshToken.for_user(user=self.student).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        self.module = Module.objects.create(teacher=self.teacher, start_time="13:00:00",
                                            end_time="14:00:00", date="2023-05-05")
        self.reservation = Reservation.objects.create(student=self.student, module=self.module, teacher_done=True, student_done=True)
        post_data = {
            "reservation": self.reservation.id,
            "amount": 15000,
            "transaction_method": "paypal"
        }

        self.token = RefreshToken.for_user(user=self.teacher).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        response = self.client.post(
            '/api/transaction/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You must be a student to perform this action")

    def test_create_transaction_on_alien_reservation(self):
        self.student = get_user_model().objects.create_user(
            mail="student@uc.cl",
            password="pass1234test",
            first_name="student",
            last_name="student",
            phone="66783359",
            is_student=True)

        self.alien = get_user_model().objects.create_user(
            mail="alien@uc.cl",
            password="pass1234test",
            first_name="alien",
            last_name="alien",
            phone="66783322",
            is_student=True)

        self.teacher = get_user_model().objects.create_user(
            mail="teacher@uc.cl",
            password="pass1234test",
            first_name="teacher",
            last_name="teacher",
            phone="66783309",
            is_teacher=True)

        self.token = RefreshToken.for_user(user=self.alien).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        self.module = Module.objects.create(teacher=self.teacher, start_time="13:00:00",
                                            end_time="14:00:00", date="2023-05-05")
        self.reservation = Reservation.objects.create(student=self.student, module=self.module, teacher_done=True, student_done=True)
        post_data = {
            "reservation": self.reservation.id,
            "amount": 15000,
            "transaction_method": "paypal"
        }
        response = self.client.post(
            '/api/transaction/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You are not the owner of this reservation")

    def test_update_transaction(self):

        self.student = get_user_model().objects.create_user(
            mail="student@uc.cl",
            password="pass1234test",
            first_name="student",
            last_name="student",
            phone="66783359",
            is_student=True)

        self.teacher = get_user_model().objects.create_user(
            mail="teacher@uc.cl",
            password="pass1234test",
            first_name="teacher",
            last_name="teacher",
            phone="66783309",
            is_teacher=True)

        self.token = RefreshToken.for_user(user=self.student).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        self.module = Module.objects.create(teacher=self.teacher, start_time="13:00:00",
                                            end_time="14:00:00", date="2023-05-05")
        self.reservation = Reservation.objects.create(student=self.student, module=self.module, teacher_done=True, student_done=True)
        post_data = {
            "reservation": self.reservation.id,
            "amount": 15000,
            "transaction_method": "paypal"
        }
        response = self.client.post(
            '/api/transaction/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response2 = self.client.patch(
            f'/api/transaction/?id={response.data["id"]}', {"amount": 10000})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["amount"], 10000)

    def test_update_alien_transaction(self):

        self.student = get_user_model().objects.create_user(
            mail="student@uc.cl",
            password="pass1234test",
            first_name="student",
            last_name="student",
            phone="66783359",
            is_student=True)

        self.alien = get_user_model().objects.create_user(
            mail="alien@uc.cl",
            password="pass1234test",
            first_name="alien",
            last_name="alien",
            phone="66783322",
            is_student=True)

        self.teacher = get_user_model().objects.create_user(
            mail="teacher@uc.cl",
            password="pass1234test",
            first_name="teacher",
            last_name="teacher",
            phone="66783309",
            is_teacher=True)

        self.token = RefreshToken.for_user(user=self.student).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        self.module = Module.objects.create(teacher=self.teacher, start_time="13:00:00",
                                            end_time="14:00:00", date="2023-05-05")
        self.reservation = Reservation.objects.create(student=self.student, module=self.module, teacher_done=True, student_done=True)
        
        self.transaction = TransactionModel.objects.create(reservation=self.reservation, student=self.alien, amount=15000, transaction_method="paypal")

        response = self.client.patch(
            f'/api/transaction/?id={self.transaction.id}', {"amount": 10000})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You are not the owner of this transaction")

    def test_delete_transaction(self):

        self.student = get_user_model().objects.create_user(
            mail="student@uc.cl",
            password="pass1234test",
            first_name="student",
            last_name="student",
            phone="66783359",
            is_student=True)

        self.teacher = get_user_model().objects.create_user(
            mail="teacher@uc.cl",
            password="pass1234test",
            first_name="teacher",
            last_name="teacher",
            phone="66783309",
            is_teacher=True)

        self.token = RefreshToken.for_user(user=self.student).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        self.module = Module.objects.create(teacher=self.teacher, start_time="13:00:00",
                                            end_time="14:00:00", date="2023-05-05")
        self.reservation = Reservation.objects.create(student=self.student, module=self.module, teacher_done=True, student_done=True)
        
        self.transaction = TransactionModel.objects.create(reservation=self.reservation, student=self.student, amount=15000, transaction_method="paypal")


        response = self.client.delete(
            f'/api/transaction/?id={self.transaction.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_alien_transaction(self):

        self.student = get_user_model().objects.create_user(
            mail="student@uc.cl",
            password="pass1234test",
            first_name="student",
            last_name="student",
            phone="66783359",
            is_student=True)

        self.alien = get_user_model().objects.create_user(
            mail="alien@uc.cl",
            password="pass1234test",
            first_name="alien",
            last_name="alien",
            phone="66783322",
            is_student=True)

        self.teacher = get_user_model().objects.create_user(
            mail="teacher@uc.cl",
            password="pass1234test",
            first_name="teacher",
            last_name="teacher",
            phone="66783309",
            is_teacher=True)

        self.token = RefreshToken.for_user(user=self.student).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        self.module = Module.objects.create(teacher=self.teacher, start_time="13:00:00",
                                            end_time="14:00:00", date="2023-05-05")
        self.reservation = Reservation.objects.create(student=self.student, module=self.module, teacher_done=True, student_done=True)
        
        self.transaction = TransactionModel.objects.create(reservation=self.reservation, student=self.alien, amount=15000, transaction_method="paypal")

        response = self.client.delete(
            f'/api/transaction/?id={self.transaction.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You are not the owner of this transaction")

    