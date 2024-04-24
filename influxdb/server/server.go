package main

import (
	"net/http"

	echo "github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"github.com/labstack/gommon/log"
)

func ok(c echo.Context) error {
	return c.String(http.StatusOK, "OK")
}

func write(c echo.Context) error {
	return c.String(http.StatusNoContent, "")
}

func writeV2(c echo.Context) error {
	return c.String(http.StatusOK, "")
}

func ping(c echo.Context) error {
	return c.String(http.StatusNoContent, "")
}

func main() {
	e := echo.New()
	e.Logger.SetLevel(log.DEBUG)
	e.Use(middleware.Logger())

	e.GET("/", ok)
	e.POST("/write", write)
	e.POST("/api/v2/write", writeV2)
	e.GET("/ping", ping)

	if err := e.Start("127.0.0.1:8086"); err != http.ErrServerClosed {
		log.Fatal(err)
	}
}
