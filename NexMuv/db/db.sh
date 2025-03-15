#!/bin/bash

## SCRIPT PARA CONFIGURAR O BANCO DE DADOS UTILIZANDO O POSTGRESQL

## nome do usuário
u=devpython

## criação do usuário
createuser -U $(whoami) -s $u

## criação da base de dados
createdb $u -U $u

## execução do script proposto
psql -U $u -f db.sql