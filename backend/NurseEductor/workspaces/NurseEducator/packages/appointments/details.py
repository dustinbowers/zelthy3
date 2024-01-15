from ...packages.crud.detail.base import BaseDetail

class AppointmentBaseDeatil(BaseDetail):
    
    def get_context_data(self, context, **kwargs):
        context = super().get_context_data(context, **kwargs)

        if self.get_object_pk():
            obj = self.get_object(self.get_object_pk())

            if obj.appointment_type == 'video':
                if obj.video_call_details:
                    context['host_join_link'] = obj.video_call_details.get('start_url', '')

        return context