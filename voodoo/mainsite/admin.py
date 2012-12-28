from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
# from django.contrib import admin
from russian_admin import admin
from voodoo.mainsite.models import MyRegistrationProfile, Profile, Prepays, OrderDispatch, Sendings, VinDetails, VinRequest, CarAdditional
from django.utils.translation import ugettext_lazy as _
# from voodoo.admin_center.models import Product, OrderItem
import voodoo


class MyRegistrationAdmin(admin.ModelAdmin):
    actions = ['activate_users', 'resend_activation_email']
    list_display = ('user', 'activation_key_expired')
    raw_id_fields = ['user']
    search_fields = ('user__username', 'user__first_name')

    def activate_users(self, request, queryset):
        """
        Activates the selected users, if they are not alrady
        activated.
        """
        for profile in queryset:
            MyRegistrationProfile.objects.activate_user(profile.activation_key)
    activate_users.short_description = _("Activate users")

    def resend_activation_email(self, request, queryset):
        """
        Re-sends activation emails for the selected users.

        Note that this will *only* send activation emails for users
        who are eligible to activate; emails will not be sent to users
        whose activation keys have expired or who have already
        activated.

        """
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        for profile in queryset:
            if not profile.activation_key_expired():
                profile.send_activation_email(site)
    resend_activation_email.short_description = _("Re-send activation emails")

admin.site.register(MyRegistrationProfile, MyRegistrationAdmin)
admin.site.register(Profile)
admin.site.register(Prepays)
admin.site.register(OrderDispatch)
admin.site.register(Sendings)
admin.site.register(VinDetails)
admin.site.register(VinRequest)
admin.site.register(CarAdditional)
# admin.site.register(Product)
# admin.site.register(Item)


#admin_center models

admin.site.register(voodoo.admin_center.models.DiscountGroup)
admin.site.register(voodoo.admin_center.models.Currency)
admin.site.register(voodoo.admin_center.models.ItemStatus)
admin.site.register(voodoo.admin_center.models.OrderStatus)
admin.site.register(voodoo.admin_center.models.OrderItem)
admin.site.register(voodoo.admin_center.models.Product)
admin.site.register(voodoo.admin_center.models.Supplier)
admin.site.register(voodoo.admin_center.models.Order)
admin.site.register(voodoo.admin_center.models.Menu)
