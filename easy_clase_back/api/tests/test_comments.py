from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Module, Reservation
from api.models import Comment as CommentModel


class Comments(APITestCase):

    def test_create_comment(self):
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
            "teacher": self.teacher.id,
            "body": "Excelente profe",
            "rating": 5.0 
        }
        response = self.client.post(
            '/api/comment/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_as_teacher(self):
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

        self.token = RefreshToken.for_user(user=self.teacher).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        self.module = Module.objects.create(teacher=self.teacher, start_time="13:00:00",
                                            end_time="14:00:00", date="2023-05-05")
        self.reservation = Reservation.objects.create(student=self.teacher, module=self.module, teacher_done=True, student_done=True)
        post_data = {
            "teacher": self.teacher.id,
            "body": "Excelente profe",
            "rating": 5.0 
        }
        response = self.client.post(
            '/api/comment/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You must be a student to perform this action")

    def test_create_comment_on_alien_reservation(self):
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
            "teacher": self.teacher.id,
            "body": "Excelente profe",
            "rating": 5.0 
        }
        response = self.client.post(
            '/api/comment/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You don't have a reservation with this teacher")

    # def test_create_comment_on_without_student_confirmation(self):
    #     self.student = get_user_model().objects.create_user(
    #         mail="student@uc.cl",
    #         password="pass1234test",
    #         first_name="student",
    #         last_name="student",
    #         phone="66783359",
    #         is_student=True)

    #     self.teacher = get_user_model().objects.create_user(
    #         mail="teacher@uc.cl",
    #         password="pass1234test",
    #         first_name="teacher",
    #         last_name="teacher",
    #         phone="66783309",
    #         is_teacher=True)

    #     self.token = RefreshToken.for_user(user=self.student).access_token
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

    #     self.module = Module.objects.create(teacher=self.teacher, start_time="13:00:00",
    #                                         end_time="14:00:00", date="2023-05-05")
    #     self.reservation = Reservation.objects.create(student=self.student, module=self.module, teacher_done=True, student_done=False)
    #     post_data = {
    #         "reservation": self.reservation.id,
    #         "body": "Excelente profe",
    #         "rating": 5.0 
    #     }
    #     response = self.client.post(
    #         '/api/comment/', post_data, 'json',
    #         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(response.data["detail"], "The student or teacher has not confirmed that this class happened")

    # def test_create_comment_on_without_teacher_confirmation(self):
    #     self.student = get_user_model().objects.create_user(
    #         mail="student@uc.cl",
    #         password="pass1234test",
    #         first_name="student",
    #         last_name="student",
    #         phone="66783359",
    #         is_student=True)

    #     self.teacher = get_user_model().objects.create_user(
    #         mail="teacher@uc.cl",
    #         password="pass1234test",
    #         first_name="teacher",
    #         last_name="teacher",
    #         phone="66783309",
    #         is_teacher=True)

    #     self.token = RefreshToken.for_user(user=self.student).access_token
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

    #     self.module = Module.objects.create(teacher=self.teacher, start_time="13:00:00",
    #                                         end_time="14:00:00", date="2023-05-05")
    #     self.reservation = Reservation.objects.create(student=self.student, module=self.module, teacher_done=False, student_done=True)
    #     post_data = {
    #         "reservation": self.reservation.id,
    #         "body": "Excelente profe",
    #         "rating": 5.0 
    #     }
    #     response = self.client.post(
    #         '/api/comment/', post_data, 'json',
    #         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(response.data["detail"], "The student or teacher has not confirmed that this class happened")
        
    def test_get_comments_with_filter(self):
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
            "teacher": self.teacher.id,
            "body": "Excelente profe",
            "rating": 4.3 
        }
        self.client.post(
            '/api/comment/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.get('/api/comments/?body=excelente')
        response2 = self.client.get('/api/comments/?rating=2.1,4.3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['body'], 'Excelente profe')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data[0]['rating'], 4.3)

    def test_update_comment(self):

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
        
        self.comment = CommentModel.objects.create(teacher=self.teacher, body="Wenisimo", rating=4.3, student=self.student, author=self.student.first_name, picture=self.student.picture)

        response = self.client.patch(
            f'/api/comment/?id={self.comment.id}', {"rating": 4.2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating"], 4.2)

    def test_update_alien_comment(self):

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
        self.reservation = Reservation.objects.create(student=self.alien, module=self.module, teacher_done=True, student_done=True)
        
        self.comment = CommentModel.objects.create(teacher=self.teacher, body="Wenisimo", rating=4.3, student=self.alien, author=self.alien.first_name, picture=self.alien.picture)

        response = self.client.patch(
            f'/api/comment/?id={self.comment.id}', {"rating": 4.3})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You are not the owner of this comment")

    def test_delete_comment(self):

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
        
        self.comment = CommentModel.objects.create(teacher=self.teacher, body="Wenisimo", rating=4.3, student=self.student, author=self.student.first_name, picture=self.student.picture)
        response = self.client.delete(
            f'/api/comment/?id={self.comment.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_alien_comment(self):

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
        self.reservation = Reservation.objects.create(student=self.alien, module=self.module, teacher_done=True, student_done=True)
        
        self.comment = CommentModel.objects.create(teacher=self.teacher, body="Wenisimo", rating=4.3, student=self.alien, author=self.alien.first_name, picture=self.alien.picture)

        response = self.client.delete(
            f'/api/comment/?id={self.comment.id}', {"rating": 4.3})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You are not the owner of this comment")