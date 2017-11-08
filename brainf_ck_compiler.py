import click


@click.command()
@click.argument('brainf_ck', type=click.File('r'))
@click.option('-o', nargs=1, type=click.File('w'))
def CCompiler(brainf_ck, o):

	bfck_dict = {
		">": "\t++ptr;\n",
       	    "<": "\t--ptr;\n",
       	    "+": "\t++(*ptr);\n",
       	    "-": "\t--(*ptr);\n",
       	    ".": """\tprintf("%c",(*ptr));\n""",
       	    ",": """\tscanf("%c",ptr);\n""",
       	    "[": """\twhile(*ptr) {\n\t""",
       	    "]": "\t\n}\n",
	}

	CInit = """#include <stdio.h>
#include <stdlib.h>

int main(void) {
	char *tape = malloc(sizeof(char)*40000);
	char *ptr = &tape[0];
"""

	source = brainf_ck.read()
	for data in source:
		if data in bfck_dict:
			CInit = CInit + bfck_dict[data]

	CInit = CInit + """\tprintf("\\n");\n\treturn 0;\n}"""

	o.write(CInit)
	o.flush()


if __name__ == "__main__":
    op = CCompiler()
