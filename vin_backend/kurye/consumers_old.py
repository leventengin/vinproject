
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.consumer import AsyncConsumer

class KuryeConsumer(AsyncConsumer):




    
    """
    def __init__(self, scope):
        super().__init__(scope)
        # Keep track of the user's trips.
        self.trips = set()
    """

    async def connect(self):
        user = self.scope['user']
        print("-----------------connect--------------------")
        print(user)
        if user.is_anonymous:
            print("anonymous")
            await self.close()
        else:
            print("not anonymous")
            await self.accept()


    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if message_type == 'upload.location':
            await self.create_trip(content)
        """
        elif message_type == 'update.trip':  
            await self.update_trip(content)
        """


    async def update_trip(self, event):
        trip = await self._update_trip(event.get('data'))
        trip_id = f'{trip.id}'
        trip_data = ReadOnlyTripSerializer(trip).data

        # Handle add only if trip is not being tracked.
        # This happens when a driver accepts a request.
        if trip_id not in self.trips:
            self.trips.add(trip_id)
            await self.channel_layer.group_add(
                group=trip_id,
                channel=self.channel_name
            )

        await self.send_json({
            'type': 'update.trip',
            'data': trip_data
        })



    async def echo_message(self, event):
        await self.send_json(event)


    async def create_trip(self, event):
        trip = await self._create_trip(event.get('data'))
        trip_id = f'{trip.id}'
        trip_data = ReadOnlyTripSerializer(trip).data

        # Add trip to set.
        self.trips.add(trip_id)

        # Add this channel to the new trip's group.
        await self.channel_layer.group_add(
            group=trip_id,
            channel=self.channel_name
        )

        await self.send_json({
            'type': 'create.trip',
            'data': trip_data
        })


    async def disconnect(self, code):
        # Remove this channel from every trip's group.
        channel_groups = [
            self.channel_layer.group_discard(
                group=trip,
                channel=self.channel_name
            )
            for trip in self.trips
        ]
        asyncio.gather(*channel_groups)

        # Remove all references to trips.
        self.trips.clear()

        await super().disconnect(code)


    @database_sync_to_async
    def _create_trip(self, content):
        serializer = TripSerializer(data=content)
        serializer.is_valid(raise_exception=True)
        trip = serializer.create(serializer.validated_data)
        return trip


    @database_sync_to_async
    def _get_trips(self, user):
        if not user.is_authenticated:
            raise Exception('User is not authenticated.')
        user_groups = user.groups.values_list('name', flat=True)
        if 'driver' in user_groups:
            return user.trips_as_driver.exclude(
                status=Trip.COMPLETED
            ).only('id').values_list('id', flat=True)
        else:
            return user.trips_as_rider.exclude(
                status=Trip.COMPLETED
            ).only('id').values_list('id', flat=True)


    @database_sync_to_async
    def _update_trip(self, content):
        instance = Trip.objects.get(id=content.get('id'))
        serializer = TripSerializer(data=content)
        serializer.is_valid(raise_exception=True)
        trip = serializer.update(instance, serializer.validated_data)
        return trip


    @database_sync_to_async
    def _create_client(self, content):
        if not user.is_authenticated:
            raise Exception('User is not authenticated.')
        if 'driver' in user_groups:
            return user.trips_as_driver.exclude(
                status=Trip.COMPLETED
            ).only('id').values_list('id', flat=True)
        else:
            return user.trips_as_rider.exclude(
                status=Trip.COMPLETED
            ).only('id').values_list('id', flat=True)

