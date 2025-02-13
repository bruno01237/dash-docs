# -*- coding: utf-8 -*-
from dash import Dash
from flask import redirect, escape, request
from dash_docs.convert_to_html import convert_to_html


class CustomDash(Dash):
    def interpolate_index(self, **kwargs):
        # import later to prevent circular imports - yikes
        from .chapter_index import URL_TO_META_MAP, URL_TO_CONTENT_MAP
        kwargs.pop('title')

        if request.path in URL_TO_META_MAP:
            name = URL_TO_META_MAP[request.path].get('breadcrumb', URL_TO_META_MAP[request.path]['name'])
            name += ' | Dash for Python Documentation | Plotly'
        else:
            name = 'Dash Documentation & User Guide | Plotly'
        meta_kwargs = dict(
            title=name,
            description=URL_TO_META_MAP.get(request.path, {}).get(
                'description', 'Plotly Dash User Guide & Documentation'
            ),
            **kwargs
        )
        if request.path in URL_TO_CONTENT_MAP:
            meta_kwargs['ssr_content'] = convert_to_html(
                URL_TO_CONTENT_MAP[request.path]
            )
        else:
            meta_kwargs['ssr_content'] = ''

        return ('''<!DOCTYPE html>
        <html>
            <head>
                {metas}
                <title>{title}</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta
                    name="description"
                    content="{description}"
                >
                <meta name="google-site-verification" content="EgLBLquJuqD_NR96F-pKLhTy9ZKQlWIoQlexW_OVKrM" />
                <title>{title}</title>
                {favicon}
                {css}
        '''.format(**meta_kwargs) + '''
                <!-- Google Tag Manager Tag -->
                <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
                new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
                j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
                'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
                })(window,document,'script','dataLayer','GTM-N6T2RXG');</script>
            </head>
            <body>
                <!-- Google Tag Manager Tag -->
                <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-N6T2RXG"
                    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
        ''' + '''
                <div id="react-entry-point">
                    {ssr_content}
                </div>
                <footer>
                    {config}
                    {scripts}
                    {renderer}
                </footer>
            </body>
        </html>'''.format(**meta_kwargs))


app = CustomDash(__name__)
server = app.server

app.config.suppress_callback_exceptions = True


@server.route('/deployment/on-premise')
def redirect_dds():
    return redirect("/dash-enterprise", code=301)


@server.route('/dash-enterprise/enviornment-variables')
def redirect_env_var():
    return redirect("/dash-enterprise/environment-variables", code=301)


@server.route('/dash-1-0-migration.')
def redirect_migration():
    return redirect("/dash-1-0-migration", code=301)


@server.route('/gallery')
def redirect_gallery():
    return redirect("https://dash-gallery.plotly.host/Portal/", code=301)


@server.route('/gallery)')
def redirect_gallery_trailing_p():
    # there is some link out there to /gallery) that appears on duck duck go
    return redirect("https://dash-gallery.plotly.host/Portal/", code=301)


@server.route('/dash-deployment-server')
def redirect_to_enterprise():
    return redirect('/dash-enterprise', code=301)


@server.route('/dash-deployment-server/<path:subpath>')
def redirect_to_enterprise_part(subpath):
    return redirect('/dash-enterprise/{}'.format(escape(subpath)), code=301)


@server.route('/dash-table')
def redirect_table():
    return redirect('/datatable', code=301)


@server.route('/dash-table/<path:subpath>')
def redirect_table_part(subpath):
    return redirect('/datatable/{}'.format(escape(subpath)), code=301)


@server.route('/daq')
def redirect_daq():
    return redirect('/dash-daq', code=301)


@server.route('/daq/<path:subpath>')
def redirect_daq_part(subpath):
    return redirect('/dash-daq/{}'.format(escape(subpath)), code=301)

# normalized components
@server.route('/dash-core-components/loading_component')
def redirect_dcc_loading():
    return redirect('/dash-core-components/loading', code=301)

@server.route('/dash-core-components/confirm-provider')
def redirect_dcc_confirm_provider():
    return redirect('/dash-core-components/confirmdialogprovider', code=301)

@server.route('/dash-core-components/confirm')
def redirect_dcc_confirm():
    return redirect('/dash-core-components/confirmdialog', code=301)

@server.route('/dash-core-components/faq')
def redirect_faq():
    return redirect('/faqs', code=301)


@server.route('/search')
def redirect_search():
    return redirect('/', code=302)


@server.route('/getting-started')
def redirect_getting_started():
    return redirect('/layout', code=301)

@server.route('/getting-started-part-2')
def redirect_getting_started_2():
    return redirect('/basic-callbacks', code=301)

@server.route('/state')
def redirect_state():
    return redirect('/basic-callbacks', code=301)

@server.route('/sizing')
def redirect_sizing():
    return redirect('/height', code=301)

@server.route('/checks')
def redirect_checks():
    return redirect('/application-structure', code=301)

@server.route('/datatable/sizing')
def redirect_datatable_sizing():
    return redirect('/datatable/width', code=301)

@server.before_request
def clear_trailing():
    rp = request.path
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])

@server.after_request
def redirect_url(response):
    url_root = 'https://dash.plotly.com'
    rp = request.path
    return redirect('{root}{path}'.format(root=url_root, path=rp))
