"""
Build statically rendered files.

SPDX-FileCopyrightText: 2021 Birger Schacht <schacht@cert.at>, Mikk Margus Möll <mikk@cert.ee>, Sebastian Wagner <wagner@cert.at>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
import argparse
import pathlib
import shutil
from mako.lookup import TemplateLookup


def render_page(pagename: str, **template_args) -> str:
    template_dir = pathlib.Path(__file__).parent / 'templates'
    template_lookup = TemplateLookup(directories=[template_dir], default_filters=["h"], input_encoding='utf8')
    template = template_lookup.get_template(f'{pagename}.mako')

    return template.render(pagename=pagename, **template_args)


def buildhtml(outputdir: pathlib.Path = pathlib.Path('html')):
    outputdir.mkdir(parents=True, exist_ok=True)

    htmlfiles = ["configs", "management", "monitor", "check", "about", "index"]
    for filename in htmlfiles:
        print(f"Rendering {filename}.html")
        html = render_page(filename)
        outputdir.joinpath(f"{filename}.html").write_text(html)

    staticfiles = ["css", "images", "js", "plugins", "less"]
    for filename in staticfiles:
        print(f"Copying {filename} recursively")
        src = pathlib.Path(__file__).parent / 'static' / filename
        dst = outputdir / filename
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    print('rendering dynvar.js')
    rendered = render_page('dynvar', allowed_path='/opt/intelmq/var/lib/bots/', controller_cmd='intelmq')
    outputdir.joinpath('js/dynvar.js').write_text(rendered)


def main():
    parser = argparse.ArgumentParser(
        prog='intelmq-manager-build',
        description='Build statically rendered files for intelmq-manager.',
        epilog='This command renders and saves all files required for IntelMQ Manager at the given directory, which can be served by Webservers statically',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('--output-dir', '-o', default='html',
                        type=pathlib.Path,
                        help='The destination directory, will be created if needed.')
    args = parser.parse_args()
    buildhtml(outputdir=args.output_dir)


if __name__ == '__main__':
    main()
