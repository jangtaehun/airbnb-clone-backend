from rest_framework.views import APIView
from .models import Perk, Experience
from .serializer import PerkSerializer, ExperienceSerializer, ExperiencePerkSerializer

from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class ExperienceList(APIView):
    def get(self, request):
        all_experience = Experience.objects.all()
        serializer = ExperienceSerializer(
            all_experience, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            new_experience = serializer.save()
            serializer = ExperienceSerializer(new_experience)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk=pk)
        serializer = ExperienceSerializer(experience)
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceSerializer(
            experience,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_experience = serializer.save()
            serializer = ExperienceSerializer(updated_experience)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk)
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperiencePerk(APIView):

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):

        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size

        experience = self.get_object(pk)
        perks = experience.perks.all()
        # experience에 있는 perks에 대한 정보를 가져온다.
        print(perks)
        serializer = PerkSerializer(
            perks[start:end],
            many=True,
        )
        return Response(serializer.data)

    # Serializer의 인스턴스는 모델 인스턴스나 쿼리셋 등을 인자로 받아야 한다.
    # ExperiencePerkSerializer가 처리한 데이터를 PerkSerializer에 넘겨주어야 한다.


class ExperienceBooking(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        pass


class Perks(APIView):
    def get(self, request):
        all_perk = Perk.objects.all()
        serializer = PerkSerializer(all_perk, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request)
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            new_perk = serializer.save()
            return Response(PerkSerializer(new_perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):

    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)
