
from rest_framework import views, status
from rest_framework.response import Response

from .models import Location, Register, Meter, Host, AssignedMeasurement, Measurement
from .serializers import LocationSerializer, MeterSerializer, HostSerializer, AssignedMeasurementSerializer, MeasurementSerializer, RegisterSerializer
from .permissions import DoesRequestingUserExist, IsLocationOwner


"""
API endpoints for regular users, regular user is only allowed to have all access to Locations and ChosenMeasurements
"""


class LocationAPI(views.APIView):
    permission_classes = [DoesRequestingUserExist, IsLocationOwner, ]


    """ getting all locations of authenticated user """
    def get(self, request, format=None):
        locations = Location.objects.filter(user=request.user.id)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    """ adding new location for authenticated user """
    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: put and delete


class AssignedMeasurementAPI(views.APIView):
    permission_classes = [DoesRequestingUserExist, ]


    """ getting all chosen measurements of certain host, user needs to be authenticated """
    def get(self, request, host_id, format=None):

        try:
            host = Host.objects.get(id=host_id)
        except Host.DoesNotExist:
            return Response({"error": "Host with id {0} does not exist".format(host_id)}, status=status.HTTP_404_NOT_FOUND)

        # TODO: move this to permission
        if host.user != request.user:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        chosen_measurements = AssignedMeasurement.objects.filter(host=host_id)
        serializer = AssignedMeasurementSerializer(chosen_measurements, many=True)
        return Response(serializer.data)

    """ adding measurements for certain host """
    def post(self, request, host_id, format=None):

        try:
            host = Host.objects.get(id=host_id)
        except Host.DoesNotExist:
            return Response({"error": "Host with id {0} does not exist".format(host_id)},
                            status=status.HTTP_404_NOT_FOUND)

        # TODO: move this to permission
        if host.user != request.user:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        # TODO: move this to serializer
        data = []
        for measurement in request.data['measurements']:
            partial_data = {
                "host": host.id,
                "measurement": measurement
            }
            data.append(partial_data)

        serializer = AssignedMeasurementSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: put and delete



class MeterAPI(views.APIView):
    permission_classes = [DoesRequestingUserExist, ]

    """ getting all available energy meters, user needs to be authenticated event though meter is not directly assigned to user """
    def get(self, request, format=None):
        meters = Meter.objects.all()
        serializer = MeterSerializer(meters, many=True)
        return Response(serializer.data)


class MeasurementDetailByMeterAPI(views.APIView):
    permission_classes = [DoesRequestingUserExist, ]

    """ getting all measurements available for certain meter """
    def get(self, request, meter_id, format=None):
        registers = Register.objects.filter(meter=meter_id)
        if not len(registers):
            return Response({"error": "Cannot find measurements for meter with id {0}".format(meter_id)}, status=status.HTTP_404_NOT_FOUND)


        measurements = []
        for register in registers:
            measurements.append(Measurement.objects.get(measurement=register.measurement))


        serializer = MeasurementSerializer(measurements, many=True)
        return Response(serializer.data)


class HostAPI(views.APIView):
    permission_classes = [DoesRequestingUserExist, ]

    """ getting all hosts assigned to authenticated user """
    def get(self, request, format=None):
        hosts = Host.objects.filter(user=request.user.id)
        serializer = HostSerializer(hosts, many=True)
        return Response(serializer.data)






