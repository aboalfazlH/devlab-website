from django.views.generic import View
from django.http import JsonResponse
import faker


class FakeUsersView(View):
    def get(self, request, count, *args, **kwargs):
        data = {"users": []}
        fake = faker.Faker("fa-IR")

        for _ in range(1, count + 1):
            data["users"].append(
                {
                    "username": f"u_{_}",
                    "email": fake.email(),
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "online": fake.boolean(),
                }
            )

        return JsonResponse(data, safe=False)
