##
## EPITECH PROJECT, 2021
## B-MAT-500-COT-5-1-305construction-mohamed.mazu
## File description:
## Makefile
##

NAME	=	305construction

all:	$(NAME)

$(NAME):
		ln -s 305construction.py $(NAME)
		chmod +x $(NAME)

clean:
		rm -rf *~
		rm -rf __pycache__

fclean:	clean
		rm -rf $(NAME)

re:	fclean all